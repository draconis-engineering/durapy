"""
The `DuraPy` `UniCLI` module.
This module contains the standard CLI framework from the `DuraPy` library."""

from .unicli import (
    Console,
    clear_terminal,
    console_confirm,
    console_input,
    console_msg,
    console_print,
)

_LAZY_EXPORTS = {"DuraPyREPL", "ReplRegistry", "ReplCompleter", "main"}

__all__ = [
    "Console",
    "DuraPyREPL",
    "ReplCompleter",
    "ReplRegistry",
    "clear_terminal",
    "console_confirm",
    "console_input",
    "console_msg",
    "console_print",
    "main",
]


def __getattr__(name: str):
    if name in _LAZY_EXPORTS:
        from . import repl

        return getattr(repl, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
