"""`DuraPy` `Exceptions` module.

This module contains all the shared exceptions used throughout the `DuraPy` library.
"""


class ArgumentError(Exception):
    """Error raised when the count of arguments given to a function is incorrect."""

    def __init__(self, *args):
        super().__init__(*args)


class UnitError(ValueError):
    """Error raised for invalid unit operations or dimension mismatches."""


class DimensionError(ValueError):
    """Error raised for incompatible physical dimensions."""
