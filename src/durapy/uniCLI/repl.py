"""Interactive `DuraPy` REPL.

A small, batteries-included shell for exploring the library from a terminal.
It provides tab completion for modules, functions and keyword arguments,
persistent history, and "last call" memory so a previous calculation can be
re-run with new arguments.

Run it with::

    durapy

or::

    python -m durapy.uniCLI.repl
"""

from __future__ import annotations

import argparse
import ast
import difflib
import inspect
import math
import re
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Iterable, Iterator, Sequence

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.traceback import Traceback

MODULE_NAMES: tuple[str, ...] = (
    "unimath",
    "uniphys",
    "unisky",
    "unichem",
    "unipower",
    "uniops",
    "unibio",
    "unicogni",
    "unicrypto",
)

COMMANDS: dict[str, str] = {
    "help": "Show commands and usage",
    "modules": "List available modules",
    "list": "List functions/classes, optionally for one module",
    "doc": "Show the signature and docstring for a function",
    "src": "Show the source of a function",
    "last": "Show the previous call",
    "again": "Re-run the previous call, optionally with new arguments",
    "history": "Show this session's input history",
    "clear": "Clear the screen",
    "traceback": "Toggle full tracebacks",
    "quit": "Exit the REPL",
}

COMMAND_ALIASES: dict[str, str] = {
    "h": "help",
    "?": "help",
    "mods": "modules",
    "ls": "list",
    "d": "doc",
    "rerun": "again",
    "hist": "history",
    "cls": "clear",
    "tb": "traceback",
    "q": "quit",
    "exit": "quit",
}

STYLE = Style.from_dict(
    {
        "prompt": "bold cyan",
        "completion-menu.completion": "bg:#1e1e1e #d0d0d0",
        "completion-menu.completion.current": "bg:#005f87 #ffffff",
        "completion-menu.meta.completion": "bg:#1e1e1e #808080",
        "completion-menu.meta.completion.current": "bg:#005f87 #ffffff",
    }
)

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")
_ARG_SPLIT = re.compile(r"[\s,]+")


class _NotPython(Exception):
    """Raised internally when a line is not valid Python."""


@dataclass(frozen=True)
class Entry:
    """A callable discovered in the `DuraPy` namespace."""

    name: str
    obj: Callable[..., Any]
    kind: str
    module: str

    @property
    def short_name(self) -> str:
        return self.name.rsplit(".", 1)[-1]

    def signature(self) -> str:
        try:
            return f"{self.short_name}{inspect.signature(self.obj)}"
        except (TypeError, ValueError):
            return self.short_name


@dataclass
class LastCall:
    """A re-runnable record of the most recent function call."""

    name: str
    func: Callable[..., Any]
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = field(default_factory=dict)
    source: str = ""
    result: Any = None
    replay_source: bool = False
    namespace: dict[str, Any] | None = field(default=None, repr=False)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if args or kwargs:
            self.args = args
            self.kwargs = kwargs
            self.replay_source = False
        if self.replay_source and self.source and self.namespace is not None:
            self.result = eval(self.source, self.namespace)
        else:
            self.result = self.func(*self.args, **self.kwargs)
        return self.result

    def describe(self) -> str:
        if self.replay_source and not self.args and not self.kwargs:
            return self.source
        parts = [repr(arg) for arg in self.args]
        parts.extend(f"{key}={value!r}" for key, value in self.kwargs.items())
        return f"{self.short_name}({', '.join(parts)})"

    @property
    def short_name(self) -> str:
        return self.name.rsplit(".", 1)[-1]


class ReplRegistry:
    """Discovers callables exported by the `DuraPy` domain modules."""

    def __init__(self, module_names: Sequence[str] = MODULE_NAMES) -> None:
        self.module_names = tuple(module_names)
        self.entries: dict[str, Entry] = {}
        self.aliases: dict[str, str] = {}
        self.submodules: dict[str, ModuleType] = {}
        self._submodule_prefix: dict[str, str] = {}
        self._short: dict[str, list[str]] = {}
        self._submodule_candidates: dict[str, list[tuple[str, ModuleType]]] = {}
        self._visited: set[int] = set()
        self.modules: dict[str, ModuleType] = {}
        self._build()

    def _build(self) -> None:
        import durapy

        for name in self.module_names:
            module = getattr(durapy, name, None)
            if not isinstance(module, ModuleType):
                continue
            self.modules[name] = module
            self._walk(module, name, name)

        for qualified in self.entries:
            self._short.setdefault(qualified.rsplit(".", 1)[-1], []).append(qualified)

        unique = {
            name: candidates[0]
            for name, candidates in self._submodule_candidates.items()
            if len(candidates) == 1 and name not in self.modules
        }
        self.submodules = {name: module for name, (_, module) in unique.items()}
        self._submodule_prefix = {name: prefix for name, (prefix, _) in unique.items()}

        for short, prefix in self._submodule_prefix.items():
            for qualified in self.entries:
                if not qualified.startswith(prefix + "."):
                    continue
                alias = short + qualified[len(prefix) :]
                if alias not in self.entries:
                    self.aliases.setdefault(alias, qualified)

    def _walk(self, module: ModuleType, module_name: str, prefix: str) -> None:
        if id(module) in self._visited:
            return
        self._visited.add(id(module))

        names = getattr(module, "__all__", None)
        if names is None:
            names = [name for name in dir(module) if not name.startswith("_")]

        for name in names:
            if name.startswith("_"):
                continue
            try:
                obj = getattr(module, name)
            except Exception:
                continue

            qualified = f"{prefix}.{name}"
            if isinstance(obj, ModuleType):
                if obj.__name__.startswith("durapy."):
                    self._submodule_candidates.setdefault(name, []).append(
                        (qualified, obj)
                    )
                    self._walk(obj, module_name, qualified)
                continue

            if inspect.isclass(obj):
                kind = "class"
            elif inspect.isfunction(obj) or inspect.isbuiltin(obj):
                kind = "function"
            else:
                continue

            origin = getattr(obj, "__module__", "")
            if origin and not origin.startswith("durapy"):
                continue

            self.entries.setdefault(
                qualified, Entry(qualified, obj, kind, module_name)
            )

    def resolve(self, name: str) -> Entry:
        """Resolve a bare, qualified, or unambiguous name."""
        entry = self.entries.get(name)
        if entry is not None:
            return entry

        alias = self.aliases.get(name)
        if alias is not None:
            return self.entries[alias]

        candidates = self._short.get(name, [])
        if len(candidates) == 1:
            return self.entries[candidates[0]]
        if len(candidates) > 1:
            options = ", ".join(sorted(candidates))
            raise KeyError(f"'{name}' is ambiguous; use one of: {options}")
        raise KeyError(f"unknown name '{name}'")

    def resolve_quiet(self, name: str) -> Entry | None:
        try:
            return self.resolve(name)
        except KeyError:
            return None

    def unique_short_names(self) -> dict[str, str]:
        return {
            short: qualified[0]
            for short, qualified in self._short.items()
            if len(qualified) == 1
        }

    def names(self) -> list[str]:
        """All names usable for completion or suggestions."""
        names = set(self.entries)
        names.update(self.aliases)
        names.update(self.unique_short_names())
        names.update(self.modules)
        names.update(self.submodules)
        names.update({"Quantity", "Unit", "Dimension", "Constant"})
        return sorted(names)

    def completion_items(self) -> Iterator[tuple[str, str]]:
        """Yield ``(name, metadata)`` pairs for completion."""
        for name, entry in self.entries.items():
            yield name, f"{entry.kind} · {entry.module}"
        for alias, qualified in self.aliases.items():
            entry = self.entries[qualified]
            yield alias, f"{entry.kind} · {entry.module}"
        for short, qualified in self.unique_short_names().items():
            entry = self.entries[qualified]
            yield short, f"{entry.kind} · {entry.module}"
        for name in self.modules:
            yield name, "module"
        for name in self.submodules:
            yield name, "submodule"
        for name in ("Quantity", "Unit", "Dimension", "Constant"):
            yield name, "class · shared"
        for name in ("units", "constants"):
            yield name, "namespace"


class ReplCompleter(Completer):
    """Completion for function names, commands, and keyword arguments."""

    def __init__(self, repl: DuraPyREPL) -> None:
        self.repl = repl

    def get_completions(
        self, document: Document, complete_event: Any = None
    ) -> Iterator[Completion]:
        text = document.text_before_cursor
        stripped = text.lstrip()

        if not stripped:
            return

        if stripped.startswith((":", "/")):
            prefix = stripped[0]
            word = _last_word(stripped)
            for command, description in COMMANDS.items():
                candidate = prefix + command
                if candidate.lower().startswith(word.lower()):
                    yield Completion(
                        candidate,
                        start_position=-len(word),
                        display_meta=description,
                    )
            return

        open_paren = text.rfind("(")
        close_paren = text.rfind(")")
        if open_paren > close_paren:
            head = text[:open_paren].strip().split()
            if not head:
                return
            entry = self.repl.registry.resolve_quiet(head[-1])
            if entry is not None:
                arg_text = text[open_paren + 1 :]
                yield from self._parameter_completions(entry, arg_text)
            return

        parts = text.split(None, 1)
        if len(parts) == 2:
            entry = self.repl.registry.resolve_quiet(parts[0])
            if entry is not None:
                yield from self._parameter_completions(entry, parts[1])
                return
        elif text.endswith(" "):
            entry = self.repl.registry.resolve_quiet(parts[0])
            if entry is not None:
                yield from self._parameter_completions(entry, "")
                return

        word = _last_word(stripped)
        for name, meta in self.repl.registry.completion_items():
            if name.lower().startswith(word.lower()):
                yield Completion(name, start_position=-len(word), display_meta=meta)

    def _parameter_completions(
        self, entry: Entry, arg_text: str
    ) -> Iterator[Completion]:
        try:
            signature = inspect.signature(entry.obj)
        except (TypeError, ValueError):
            return

        word = _last_word(arg_text) if not arg_text.endswith((" ", ",")) else ""
        used = {
            token.split("=", 1)[0]
            for token in _ARG_SPLIT.split(arg_text)
            if "=" in token
        }

        for name, parameter in signature.parameters.items():
            if name in used or name in {"self", "cls"}:
                continue
            if parameter.kind in {
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
                inspect.Parameter.POSITIONAL_ONLY,
            }:
                continue

            candidate = f"{name}="
            if not candidate.startswith(word):
                continue

            meta = parameter.annotation
            if meta is inspect.Parameter.empty:
                meta = "parameter"
            elif not isinstance(meta, str):
                meta = getattr(meta, "__name__", str(meta))
            yield Completion(candidate, start_position=-len(word), display_meta=meta)


def _last_word(text: str) -> str:
    parts = _ARG_SPLIT.split(text.rstrip())
    return parts[-1] if parts else ""


def _literal(text: str) -> Any:
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        pass
    try:
        return float(text)
    except ValueError:
        return text


def _no_last_call(*args: Any, **kwargs: Any) -> Any:
    raise RuntimeError("No previous function call yet; call a function first.")


class DuraPyREPL:
    """A `prompt_toolkit` REPL over the `DuraPy` public API."""

    def __init__(
        self,
        *,
        history_path: Path | str | None = None,
        banner: bool = True,
        console: Console | None = None,
    ) -> None:
        self.registry = ReplRegistry()
        self.console = console or Console()
        self.history_path = (
            Path(history_path)
            if history_path is not None
            else Path.home() / ".durapy" / "history"
        )
        self.banner = banner
        self.show_traceback = False
        self._last: LastCall | None = None
        self._lines: list[str] = []
        self._should_exit = False
        self._session: PromptSession[str] | None = None

        import durapy
        from durapy.shared import constants, units
        from durapy.shared.numval_types import Constant, Dimension, Quantity, Unit

        self.namespace: dict[str, Any] = {
            "__name__": "__durapy_repl__",
            "durapy": durapy,
            "math": math,
            "units": units,
            "constants": constants,
            "Quantity": Quantity,
            "Unit": Unit,
            "Dimension": Dimension,
            "Constant": Constant,
            "last": _no_last_call,
            "_": None,
            "_fn": None,
        }
        for name, module in self.registry.modules.items():
            self.namespace[name] = module
        for name, module in self.registry.submodules.items():
            self.namespace.setdefault(name, module)

    @property
    def last_call(self) -> LastCall | None:
        return self._last

    def execute(self, line: str) -> Any:
        """Evaluate one line and return its result, if any."""
        line = line.strip()
        if not line:
            return None

        if line.startswith("?"):
            return self._cmd_doc(line[1:].strip())

        if line.startswith((":", "/")):
            return self._dispatch(line[1:].strip())

        if _IDENTIFIER.match(line) and line not in self.namespace:
            entry = self.registry.resolve_quiet(line)
            if entry is not None:
                self._print_signature(entry)
                return entry.obj

        try:
            return self._eval_python(line)
        except _NotPython:
            return self._eval_shorthand(line)

    def _eval_python(self, line: str) -> Any:
        try:
            tree = ast.parse(line, mode="eval")
        except SyntaxError:
            try:
                statement = ast.parse(line, mode="exec")
            except SyntaxError as exc:
                raise _NotPython from exc

            try:
                exec(compile(statement, "<durapy>", "exec"), self.namespace)
            except Exception as exc:
                self._show_error(exc)
            return None

        try:
            result = eval(compile(tree, "<durapy>", "eval"), self.namespace)
        except Exception as exc:
            self._show_error(exc)
            return None

        return self._handle_result(result, self._record_from_ast(tree, line))

    def _eval_shorthand(self, line: str) -> Any:
        try:
            tokens = shlex.split(line)
        except ValueError as exc:
            self._show_error(exc)
            return None

        if not tokens:
            return None

        name, *rest = tokens
        entry = self._resolve(name)
        if entry is None:
            return None

        args, kwargs = self._parse_arguments(rest)
        try:
            result = entry.obj(*args, **kwargs)
        except TypeError as exc:
            self._show_error(exc)
            self._print_signature(entry)
            return None
        except Exception as exc:
            self._show_error(exc)
            return None

        record = LastCall(
            name=entry.name,
            func=entry.obj,
            args=args,
            kwargs=kwargs,
            source=line,
            namespace=self.namespace,
        )
        return self._handle_result(result, record)

    def _parse_arguments(
        self, tokens: Iterable[str]
    ) -> tuple[tuple[Any, ...], dict[str, Any]]:
        args: list[Any] = []
        kwargs: dict[str, Any] = {}
        for token in tokens:
            key, separator, value = token.partition("=")
            if separator and key.isidentifier():
                kwargs[key] = _literal(value)
            else:
                args.append(_literal(token))
        return tuple(args), kwargs

    def _record_from_ast(self, tree: ast.Expression, source: str) -> LastCall | None:
        node = tree.body
        if not isinstance(node, ast.Call):
            return None

        name = _ast_name(node.func)
        if name is None:
            return None
        entry = self.registry.resolve_quiet(name)
        if entry is None:
            return None

        args: list[Any] = []
        kwargs: dict[str, Any] = {}
        for argument in node.args:
            value, ok = _literal_node(argument)
            if not ok:
                return LastCall(
                    name=entry.name,
                    func=entry.obj,
                    source=source,
                    replay_source=True,
                    namespace=self.namespace,
                )
            args.append(value)

        for keyword in node.keywords:
            if keyword.arg is None:
                return LastCall(
                    name=entry.name,
                    func=entry.obj,
                    source=source,
                    replay_source=True,
                    namespace=self.namespace,
                )
            value, ok = _literal_node(keyword.value)
            if not ok:
                return LastCall(
                    name=entry.name,
                    func=entry.obj,
                    source=source,
                    replay_source=True,
                    namespace=self.namespace,
                )
            kwargs[keyword.arg] = value

        return LastCall(
            name=entry.name,
            func=entry.obj,
            args=tuple(args),
            kwargs=kwargs,
            source=source,
            namespace=self.namespace,
        )

    def _handle_result(self, result: Any, record: LastCall | None = None) -> Any:
        self.namespace["_"] = result
        if record is not None:
            record.result = result
            self._last = record
            self.namespace["_fn"] = record.func
            self.namespace["last"] = record

        if result is not None:
            self.console.print(self._format_result(result))
        return result

    def _format_result(self, result: Any) -> RenderableType:
        from durapy.shared.numval_types import Quantity

        if isinstance(result, Quantity):
            return Text(str(result), style="bold")
        if isinstance(result, str):
            return Text.from_ansi(result)
        return Pretty(result, expand_all=False)

    def _show_error(self, exc: BaseException) -> None:
        if self.show_traceback:
            self.console.print(
                Traceback.from_exception(
                    type(exc), exc, exc.__traceback__, show_locals=False
                )
            )
        else:
            self.console.print(Text(f"{type(exc).__name__}: {exc}", style="bold red"))

    def _resolve(self, name: str) -> Entry | None:
        try:
            return self.registry.resolve(name)
        except KeyError as exc:
            self.console.print(Text(str(exc), style="bold red"))
            matches = difflib.get_close_matches(name, self.registry.names(), n=3)
            if matches:
                self.console.print(
                    Text("Did you mean: " + ", ".join(matches), style="yellow")
                )
            return None

    def _unknown_name(self, name: str) -> None:
        self._resolve(name)

    def _print_signature(self, entry: Entry) -> None:
        try:
            signature = str(inspect.signature(entry.obj))
        except (TypeError, ValueError):
            signature = "(...)"
        doc = inspect.getdoc(entry.obj) or ""
        body = Text(f"{entry.name}{signature}", style="bold cyan")
        if doc:
            body.append("\n\n" + doc)
        self.console.print(Panel(body, title=entry.kind, border_style="cyan"))

    def _dispatch(self, text: str) -> Any:
        if not text:
            return None

        name, _, argument = text.partition(" ")
        name = name.lower()
        canonical = COMMAND_ALIASES.get(name, name)
        handler = getattr(self, f"_cmd_{canonical}", None)
        if handler is None:
            self.console.print(Text(f"Unknown command: :{name}", style="bold red"))
            self._cmd_help()
            return None
        return handler(argument.strip())

    def _cmd_help(self, _: str = "") -> None:
        table = Table(title="Commands", border_style="cyan")
        table.add_column("Command", style="bold cyan", no_wrap=True)
        table.add_column("Description")
        for command, description in COMMANDS.items():
            table.add_row(f":{command}", description)
        self.console.print(table)
        self.console.print(
            Text(
                "Python expressions work too. Call functions as "
                "'mach_number 340' or 'mach_number(340)'.",
                style="dim",
            )
        )

    def _cmd_modules(self, _: str = "") -> None:
        table = Table(title="Modules", border_style="cyan")
        table.add_column("Module", style="bold cyan", no_wrap=True)
        table.add_column("Functions", justify="right")
        table.add_column("Classes", justify="right")
        for name in self.registry.module_names:
            entries = [
                entry
                for entry in self.registry.entries.values()
                if entry.module == name
            ]
            if not entries and name not in self.registry.modules:
                continue
            functions = sum(entry.kind == "function" for entry in entries)
            classes = sum(entry.kind == "class" for entry in entries)
            table.add_row(name, str(functions), str(classes))
        self.console.print(table)

    def _cmd_list(self, argument: str = "") -> None:
        prefix = argument.strip()
        entries = sorted(
            (
                entry
                for entry in self.registry.entries.values()
                if not prefix
                or entry.module == prefix
                or entry.name.startswith(prefix)
            ),
            key=lambda entry: entry.name,
        )
        if not entries:
            self.console.print(Text(f"No matches for {prefix!r}", style="yellow"))
            return

        table = Table(border_style="cyan")
        table.add_column("Name", style="bold cyan", no_wrap=True)
        table.add_column("Kind", no_wrap=True)
        table.add_column("Signature")
        for entry in entries:
            table.add_row(entry.name, entry.kind, entry.signature())
        self.console.print(table)

    def _cmd_doc(self, argument: str = "") -> None:
        if not argument:
            self.console.print(Text("Usage: :doc <function>", style="yellow"))
            return
        entry = self.registry.resolve_quiet(argument)
        if entry is None:
            self._unknown_name(argument)
            return
        self._print_signature(entry)

    def _cmd_src(self, argument: str = "") -> None:
        if not argument:
            self.console.print(Text("Usage: :src <function>", style="yellow"))
            return
        entry = self.registry.resolve_quiet(argument)
        if entry is None:
            self._unknown_name(argument)
            return
        try:
            source = inspect.getsource(entry.obj)
        except (OSError, TypeError) as exc:
            self._show_error(exc)
            return
        self.console.print(
            Syntax(source, "python", theme="monokai", line_numbers=True)
        )

    def _cmd_last(self, _: str = "") -> None:
        if self._last is None:
            self.console.print(Text("No function has been called yet.", style="yellow"))
            return
        self.console.print(
            Text(f"{self._last.describe()} -> {self._last.result!r}", style="bold")
        )

    def _cmd_again(self, argument: str = "") -> Any:
        if self._last is None:
            self.console.print(Text("No function has been called yet.", style="yellow"))
            return None

        if argument:
            try:
                tokens = shlex.split(argument)
            except ValueError as exc:
                self._show_error(exc)
                return None
            args, kwargs = self._parse_arguments(tokens)
            result = self._last(*args, **kwargs)
        else:
            result = self._last()

        self.namespace["_"] = result
        if result is not None:
            self.console.print(self._format_result(result))
        return result

    def _cmd_history(self, _: str = "") -> None:
        if not self._lines:
            self.console.print(Text("No history in this session.", style="yellow"))
            return
        table = Table(border_style="cyan")
        table.add_column("#", justify="right", style="dim")
        table.add_column("Input")
        for index, line in enumerate(self._lines, start=1):
            table.add_row(str(index), line)
        self.console.print(table)

    def _cmd_clear(self, _: str = "") -> None:
        self.console.clear()

    def _cmd_traceback(self, argument: str = "") -> None:
        value = argument.strip().lower()
        if value in {"on", "1", "true", "yes"}:
            self.show_traceback = True
        elif value in {"off", "0", "false", "no"}:
            self.show_traceback = False
        else:
            self.show_traceback = not self.show_traceback
        state = "on" if self.show_traceback else "off"
        self.console.print(Text(f"Tracebacks: {state}", style="cyan"))

    def _cmd_quit(self, _: str = "") -> None:
        self._should_exit = True

    def _build_session(self) -> PromptSession[str]:
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        bindings = KeyBindings()

        @bindings.add("c-space")
        def _(event: Any) -> None:
            event.current_buffer.start_completion(select_first=False)

        @bindings.add("c-l")
        def _(event: Any) -> None:
            event.app.renderer.clear()

        return PromptSession(
            message=[("class:prompt", "durapy> ")],
            completer=ReplCompleter(self),
            complete_while_typing=True,
            auto_suggest=AutoSuggestFromHistory(),
            history=FileHistory(str(self.history_path)),
            key_bindings=bindings,
            style=STYLE,
        )

    def _print_banner(self) -> None:
        import durapy

        body = Text()
        body.append(
            f"DuraPy {durapy.__version__} interactive shell\n", style="bold cyan"
        )
        body.append("Tab completes names and keyword arguments.\n", style="dim")
        body.append(
            "Up/Down recalls history; Ctrl-Space opens completion.\n\n",
            style="dim",
        )
        body.append("Try:\n", style="bold")
        for example in (
            "mach_number 340",
            "slope 0 0 2 4",
            "thermodynamics.ideal_gas_law V=0.022414 n=1.0 T=273.15",
            ":again 680",
            "last(680)",
            "_",
        ):
            body.append(f"  {example}\n", style="cyan")
        body.append("\n:help for all commands, :quit to exit.", style="dim")
        self.console.print(Panel(body, border_style="cyan", title="DuraPy REPL"))

    def run(self) -> None:
        if self.banner:
            self._print_banner()

        self._session = self._build_session()
        while not self._should_exit:
            try:
                line = self._session.prompt()
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

            self._lines.append(line)
            try:
                self.execute(line)
            except KeyboardInterrupt:
                self.console.print(Text("Cancelled.", style="yellow"))

        self.console.print(Text("Goodbye.", style="dim"))


def _ast_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _ast_name(node.value)
        if parent is None:
            return None
        return f"{parent}.{node.attr}"
    return None


def _literal_node(node: ast.AST) -> tuple[Any, bool]:
    try:
        return ast.literal_eval(node), True
    except (ValueError, SyntaxError):
        return None, False


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="durapy",
        description="Interactive DuraPy REPL with completion and last-call memory.",
    )
    parser.add_argument(
        "--history",
        type=Path,
        default=None,
        help="Path to the history file (default: ~/.durapy/history)",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Do not print the startup banner",
    )
    parser.add_argument(
        "-c",
        "--command",
        default=None,
        help="Execute a single line and exit",
    )
    args = parser.parse_args(argv)

    repl = DuraPyREPL(history_path=args.history, banner=not args.no_banner)
    if args.command:
        repl.execute(args.command)
        return 0

    repl.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
