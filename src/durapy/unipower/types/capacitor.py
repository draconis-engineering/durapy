"""Capacitor model for the `UniPower` module."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ...shared.numval_types import Quantity
from ...shared.units import COULOMB, JOULE, OHM, SECOND


@dataclass(frozen=True)
class Capacitor:
    """An ideal (plus optional ESR) capacitor.

    Parameters
    ----------
    capacitance:
        Capacitance in farads (F).
    voltage_rating:
        Maximum working voltage in volts (V). Optional.
    esr:
        Equivalent series resistance in ohms (Ω). Defaults to 0.
    """

    capacitance: float
    voltage_rating: float | None = None
    esr: float = 0.0

    def __post_init__(self) -> None:
        if self.capacitance <= 0:
            raise ValueError("capacitance must be positive")
        if self.voltage_rating is not None and self.voltage_rating <= 0:
            raise ValueError("voltage_rating must be positive")
        if self.esr < 0:
            raise ValueError("esr cannot be negative")

    def charge(self, voltage: float) -> Quantity:
        """Charge stored at ``voltage`` in coulombs (Q = C·V)."""
        return Quantity(self.capacitance * voltage, COULOMB)

    def energy(self, voltage: float) -> Quantity:
        """Energy stored at ``voltage`` in joules (E = ½·C·V²)."""
        return Quantity(0.5 * self.capacitance * voltage**2, JOULE)

    def time_constant(self, resistance: float) -> Quantity:
        """RC time constant with the given series ``resistance`` (τ = R·C)."""
        if resistance < 0:
            raise ValueError("resistance cannot be negative")
        return Quantity(resistance * self.capacitance, SECOND)

    def reactance(self, frequency: float) -> Quantity:
        """Capacitive reactance at ``frequency`` in hertz (Xc = 1 / (2π·f·C))."""
        if frequency <= 0:
            raise ValueError("frequency must be positive")
        return Quantity(1 / (2 * math.pi * frequency * self.capacitance), OHM)

    def impedance(self, frequency: float) -> complex:
        """Complex impedance at ``frequency`` (Z = -j / (2π·f·C))."""
        if frequency <= 0:
            raise ValueError("frequency must be positive")
        return complex(0.0, -1 / (2 * math.pi * frequency * self.capacitance))

    def is_within_rating(self, voltage: float) -> bool:
        """Whether ``voltage`` stays within the working voltage rating."""
        if self.voltage_rating is None:
            return True
        return abs(voltage) <= self.voltage_rating
