"""Inductor model for the `UniPower` module."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ...shared.numval_types import Quantity
from ...shared.units import HERTZ, JOULE, OHM, SECOND


@dataclass(frozen=True)
class Inductor:
    """An inductor with an optional rated current and DC series resistance.

    Parameters
    ----------
    inductance:
        Inductance in henrys (H).
    current_rating:
        Maximum continuous current in amperes (A). Optional.
    resistance:
        DC winding resistance in ohms (Ω). Defaults to 0.
    """

    inductance: float
    current_rating: float | None = None
    resistance: float = 0.0

    def __post_init__(self) -> None:
        if self.inductance <= 0:
            raise ValueError("inductance must be positive")
        if self.current_rating is not None and self.current_rating <= 0:
            raise ValueError("current_rating must be positive")
        if self.resistance < 0:
            raise ValueError("resistance cannot be negative")

    def energy(self, current: float) -> Quantity:
        """Magnetic energy stored at ``current`` in joules (E = ½·L·I²)."""
        return Quantity(0.5 * self.inductance * current**2, JOULE)

    def time_constant(self, resistance: float) -> Quantity:
        """RL time constant with the given ``resistance`` (τ = L / R)."""
        if resistance <= 0:
            raise ValueError("resistance must be positive")
        return Quantity(self.inductance / resistance, SECOND)

    def reactance(self, frequency: float) -> Quantity:
        """Inductive reactance at ``frequency`` in hertz (Xʟ = 2π·f·L)."""
        if frequency <= 0:
            raise ValueError("frequency must be positive")
        return Quantity(2 * math.pi * frequency * self.inductance, OHM)

    def impedance(self, frequency: float) -> complex:
        """Complex impedance at ``frequency`` (Z = j·2π·f·L)."""
        if frequency <= 0:
            raise ValueError("frequency must be positive")
        return complex(0.0, 2 * math.pi * frequency * self.inductance)

    def resonant_frequency(self, capacitance: float) -> Quantity:
        """Resonant frequency with ``capacitance`` in hertz (f = 1 / (2π·√(L·C)))."""
        if capacitance <= 0:
            raise ValueError("capacitance must be positive")
        return Quantity(
            1 / (2 * math.pi * math.sqrt(self.inductance * capacitance)), HERTZ
        )

    def is_within_rating(self, current: float) -> bool:
        """Whether ``current`` stays within the rated current."""
        if self.current_rating is None:
            return True
        return abs(current) <= self.current_rating
