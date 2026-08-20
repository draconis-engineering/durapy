"""Exceptions for the `UniPower` module."""

from ..shared.color_system import color_text


class InvalidColors(Exception):
    """Raises when the colors passed into resistor_insight() are invalid for the given band."""

    def __init__(self, *args):
        super().__init__(
            f"Invalid colors for {color_text('resistor_insight()', 'blue')} at indices {args}"
        )
