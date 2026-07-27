"""DuraPy UniCLI Source"""

import inspect
import os
import shlex
from collections.abc import Callable

from prompt_toolkit.completion import NestedCompleter
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..shared.color_system import color_text
from ..shared.exceptions import ArgumentError
from .exceptions import (
    EmptyTokenList,
    MissingSubCommand,
    UnknownModule,
    UnknownSubCommand,
)


class ExitEnvironmentSignal(Exception):
    """Raise when the user wants to return to MAINEnv."""

    def __init__(self):
        super().__init__()


class CommandMap:
    def __init__(self):
        pass


class ArgumentMap:
    def __init__(self):
        pass


def exit_env() -> None:
    """Exit the current environment and return to MAINEnv."""
    raise ExitEnvironmentSignal


def gen_completer(Map: dict[str, dict]) -> NestedCompleter:
    """Generate a `NestedCompleter` dict with parameter names for each function."""

    completer_dict = {}

    for module, subcmd in Map.items():
        completer_dict[module] = {}
        for subcmd_name, cmd_func in subcmd.items():
            sig = inspect.signature(cmd_func)
            completer_dict[module][subcmd_name] = {
                param: None for param in sig.parameters
            }

    return NestedCompleter.from_nested_dict(completer_dict)


def tokenize(raw_cmd_str: str) -> tuple[str, str | list[float]]:
    """Tokenize a raw command string and return token list."""
    tokens = shlex.split(raw_cmd_str)
    proc_tokens: list[str | tuple[float]] = []  # Processed tokens
    for token in tokens:
        if token.startswith("[") and token.endswith("]"):
            proc_val = tuple(
                float(x.strip()) for x in token.strip("[]").split(",") if x.strip()
            )
            proc_tokens.append(proc_val)
        else:
            proc_tokens.append(token)
    return tuple(proc_tokens)


def dispatcher(
    raw_cmd_str: str,
    cmd_map: dict[str, dict[str, Callable]],
    arg_map: dict[str, dict[str, set]],
) -> Callable:
    """The main dispatcher function that takes in a raw command string, tokenizes it, verifies the tokens, validates the arguments and dispatches the command to the correct function."""
    tokens = tokenize(raw_cmd_str)
    validate_command(tokens, cmd_map, arg_map)
    module, cmd, raw_args = tokens[0], tokens[1], tokens[2:]
    args = []
    for arg in raw_args:
        if arg == "_":
            args.append(None)
        else:
            try:
                args.append(
                    float(arg)
                    if isinstance(arg, str)
                    else (float(arg) for arg in raw_args)
                )
            except ValueError:
                args.append(arg)

    return cmd_map[module][cmd](*args)


def validate_command(
    tokens: list[str | list[float]], cmd_map: dict, arg_map: dict
) -> None:
    if not tokens:
        raise EmptyTokenList()

    module = tokens[0]
    if module not in cmd_map:
        raise UnknownModule(module)

    if len(tokens) < 2:
        raise MissingSubCommand(module)

    command = tokens[1]
    if command not in cmd_map[module]:
        raise UnknownSubCommand(module, command)

    args = tokens[2:]
    if len(args) not in arg_map[module][command]:
        raise ArgumentError(
            cmd_map[module][command], len(args), arg_map[module][command]
        )


def clear_terminal() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def console_msg(
    sender: str, sender_color: str, info: str, info_color: str = "white"
) -> str:
    return f"[{color_text(sender, sender_color)}] >>> {color_text(info, info_color)}"


def console_print(
    sender: str, sender_color: str, info: str, info_color: str = "white"
) -> None:
    print(console_msg(sender, sender_color, info, info_color))


def console_input(
    sender: str, sender_color: str, prompt: str = "", prompt_color: str = "white"
) -> str | float:
    user_input = input(console_msg(sender, sender_color, prompt, prompt_color) + " ")
    try:
        return float(user_input)
    except ValueError:
        return user_input


def console_confirm(
    sender: str, sender_color: str, prompt_info: str, prompt_color: str = "white"
) -> bool:
    while True:
        user_input = (
            input(
                console_msg(sender, sender_color, prompt_info + ":", prompt_color) + " "
            )
            .lower()
            .strip()
        )
        if user_input in ["y", "ye", "yes"]:
            return True
        elif user_input in ["n", "no"]:
            return False
        else:
            print(
                f"Please enter {color_text('y', 'green')} or {color_text('n', 'red')}"
            )


class Console:
    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(spinner_name="dots"),
            TextColumn("{task.description}"),
            transient=False,  # Keeps completed tasks visible on screen
        )
        # Dictionary mapping: { "task_name": task_id }
        self.active_tasks = {}

    def __enter__(self):
        self.progress.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()

    def start_task(self, name: str):
        """Kicks off a task. Names must be unique if running concurrently."""
        if name in self.active_tasks:
            raise ValueError(f"Task '{name}' is already running.")

        task_id = self.progress.add_task(
            description=f"Starting task: {name} ...", total=None
        )
        self.active_tasks[name] = task_id

    def end_task(self, name: str, success: bool = True, error_msg: str | None = None):
        """Resolves any specific task by its unique name, regardless of order."""
        task_id = self.active_tasks.pop(name, None)

        if task_id is None:
            raise KeyError(f"No active task found with the name '{name}'.")

        if success:
            status_text = (
                f"Starting task: {name} ... [bold green]Finished![/bold green]"
            )
        else:
            status_text = f"Starting task: {name} ... [bold red]Failed![/bold red]" + (
                f" Error: {error_msg}" if error_msg else ""
            )

        self.progress.update(task_id, description=status_text, completed=True)

    def print(self, text, style):
        """Prints a message to the console with a specific style."""
        self.progress.console.print(text, style=style)
