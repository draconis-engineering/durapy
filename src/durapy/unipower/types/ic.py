"""Integrated circuit (IC) model for the `UniPower` module."""

from __future__ import annotations

from dataclasses import dataclass

from ...shared.numval_types import Quantity
from ...shared.units import WATT


@dataclass(frozen=True)
class IC:
    """A generic integrated circuit described by its package and supply rails.

    Parameters
    ----------
    part_number:
        Human-readable part identifier.
    pins:
        Number of pins in the package.
    supply_min:
        Minimum recommended supply voltage in volts.
    supply_max:
        Maximum recommended supply voltage in volts.
    """

    part_number: str = "Generic"
    pins: int = 8
    supply_min: float = 0.0
    supply_max: float = 5.5

    def __post_init__(self) -> None:
        if self.pins < 1:
            raise ValueError("pins must be at least 1")
        if self.supply_max < self.supply_min:
            raise ValueError("supply_max must be >= supply_min")

    def is_within_supply(self, voltage: float) -> bool:
        """Whether ``voltage`` lies within the recommended supply range."""
        return self.supply_min <= voltage <= self.supply_max

    def power_dissipation(self, supply_voltage: float, supply_current: float) -> Quantity:
        """Power dissipated in watts (``P = V·I``)."""
        return Quantity(abs(supply_voltage * supply_current), WATT)
