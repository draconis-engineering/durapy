"""
The `DuraPy` `UniCLI` module.
This module contains the standard command-line interface framework from the `DuraPy` library.
It provides the necessary functions and classes to create a command-line interface for the `DuraPy` library,
including command parsing, argument validation, and command dispatching.
"""

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
