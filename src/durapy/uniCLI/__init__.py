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

__all__ = [
    "Console",
    "clear_terminal",
    "console_confirm",
    "console_input",
    "console_msg",
    "console_print",
]
