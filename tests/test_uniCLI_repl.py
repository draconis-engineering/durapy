"""Tests for the interactive DuraPy REPL."""

import io

import pytest
from prompt_toolkit.document import Document
from rich.console import Console

from durapy.uniCLI.repl import DuraPyREPL, ReplCompleter, ReplRegistry


def make_repl() -> DuraPyREPL:
    console = Console(file=io.StringIO(), force_terminal=False, width=120)
    return DuraPyREPL(banner=False, console=console)


def test_registry_resolves_bare_qualified_and_alias():
    registry = ReplRegistry()
    assert registry.resolve("slope").name == "unimath.algebra.slope"
    assert registry.resolve("unisky.mach_number").name == "unisky.mach_number"
    assert (
        registry.resolve("thermodynamics.ideal_gas_law").name
        == "uniphys.classical.thermodynamics.ideal_gas_law"
    )
    assert (
        registry.resolve("classical.thermodynamics.ideal_gas_law").name
        == "uniphys.classical.thermodynamics.ideal_gas_law"
    )


def test_registry_reports_ambiguous_names():
    registry = ReplRegistry()
    with pytest.raises(KeyError):
        registry.resolve("ideal_gas_law")


def test_python_expression():
    repl = make_repl()
    assert repl.execute("2 + 2") == 4
    assert repl.namespace["_"] == 4


def test_assignment_persists():
    repl = make_repl()
    repl.execute("x = 10")
    assert repl.namespace["x"] == 10
    assert repl.execute("x * 2") == 20


def test_shorthand_and_keyword_arguments():
    repl = make_repl()
    assert repl.execute("slope 0 0 2 4") == pytest.approx(2.0)

    result = repl.execute("thermodynamics.ideal_gas_law V=0.022414 n=1.0 T=273.15")
    assert result[0] == pytest.approx(101324.86, rel=1e-4)


def test_last_call_memory_with_again():
    repl = make_repl()
    repl.execute("slope 0 0 2 4")

    last = repl.last_call
    assert last is not None
    assert last.short_name == "slope"
    assert repl.execute(":again 0 0 1 1") == pytest.approx(1.0)
    assert repl.last_call.args == (0, 0, 1, 1)


def test_last_callable_reruns_with_new_arguments():
    repl = make_repl()
    repl.execute("slope 0 0 2 4")

    assert repl.execute("last(0, 0, 4, 8)") == pytest.approx(2.0)
    assert repl.last_call.args == (0, 0, 4, 8)


def test_unknown_names_are_graceful():
    repl = make_repl()
    assert repl.execute("definitely_not_a_function 1") is None
    assert repl.execute("ideal_gas_law 1 2 3") is None


def test_commands_do_not_raise():
    repl = make_repl()
    commands = (
        ":help",
        ":modules",
        ":list",
        ":list unisky",
        ":doc slope",
        ":src slope",
        ":history",
        ":last",
        ":traceback on",
        ":traceback off",
    )
    for command in commands:
        repl.execute(command)
    assert repl.show_traceback is False


def test_completer_suggests_function_names():
    repl = make_repl()
    completer = ReplCompleter(repl)

    completions = list(completer.get_completions(Document("mach"), None))
    assert "mach_number" in {completion.text for completion in completions}


def test_completer_suggests_parameters():
    repl = make_repl()
    completer = ReplCompleter(repl)

    completions = list(completer.get_completions(Document("slope x1=0 "), None))
    assert {"y1=", "x2=", "y2="} <= {completion.text for completion in completions}

    completions = list(completer.get_completions(Document("slope("), None))
    assert "x1=" in {completion.text for completion in completions}
