"""Exceptions for the `UniPower` module."""

from ..shared.color_system import color_text


class InconsistencyError(Exception):
    """Raises when the VIR-values passed into power_dissipation() gives inconsistent values for the three formulas."""

    def __init__(self, fault: str):
        super().__init__(
            f"Inconsistency error at {color_text('power_dissipation()', 'blue')} with {color_text(fault, 'red')}"
        )


class InvalidColors(Exception):
    """Raises when the colors passed into resistor_insight() are invalid for the given band."""

    def __init__(self, *args):
        super().__init__(
            f"Invalid colors for {color_text('resistor_insight()', 'blue')} at indices {args}"
        )
