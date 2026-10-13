"""Diode model for the `UniPower` module."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ...shared.constants import BOLTZMANN
from ...shared.numval_types import Quantity
from ...shared.units import WATT

# Elementary charge in coulombs (exact, SI 2019).
ELECTRON_CHARGE = 1.602176634e-19


@dataclass(frozen=True)
class Diode:
    """A diode described by the Shockley ideal-diode equation.

    Parameters
    ----------
    forward_voltage:
        Nominal forward drop in volts, used for the piecewise-linear model.
    saturation_current:
        Reverse saturation current ``Is`` in amperes. Defaults to 1 nA.
    ideality:
        Ideality (emission) factor ``n``. 1.0 for an ideal diode.
    breakdown_voltage:
        Reverse breakdown voltage magnitude in volts. Optional.
    """

    forward_voltage: float = 0.7
    saturation_current: float = 1e-12
    ideality: float = 1.0
    breakdown_voltage: float | None = None

    def __post_init__(self) -> None:
        if self.forward_voltage < 0:
            raise ValueError("forward_voltage cannot be negative")
        if self.saturation_current <= 0:
            raise ValueError("saturation_current must be positive")
        if self.ideality <= 0:
            raise ValueError("ideality must be positive")
        if self.breakdown_voltage is not None and self.breakdown_voltage <= 0:
            raise ValueError("breakdown_voltage must be positive")

    def thermal_voltage(self, temperature: float = 300.0) -> float:
        """Thermal voltage ``Vt = k·T / q`` in volts (default 300 K)."""
        if temperature <= 0:
            raise ValueError("temperature must be positive (kelvin)")
        return BOLTZMANN.value * temperature / ELECTRON_CHARGE

    def shockley_current(self, voltage: float, temperature: float = 300.0) -> float:
        """Current in amperes from the Shockley equation.

        ``I = Is·(exp(V / (n·Vt)) - 1)``. Saturates to ``+inf``/``-Is`` for
        extreme forward/reverse voltages rather than overflowing.
        """
        vt = self.thermal_voltage(temperature) * self.ideality
        exponent = voltage / vt
        if exponent > 700:  # exp overflow guard
            return math.inf
        return self.saturation_current * math.expm1(exponent)

    def forward_current(
        self,
        voltage: float,
        temperature: float = 300.0,
        forward_resistance: float = 0.0,
    ) -> float:
        """Current in amperes using a piecewise-linear forward model.

        Below the knee (``V < forward_voltage``) the Shockley equation is used.
        Above it, the diode is modelled as a fixed ``forward_voltage`` drop in
        series with ``forward_resistance``. With the default zero resistance an
        ideal diode conducts any current at that drop (returns ``inf``).
        """
        if forward_resistance < 0:
            raise ValueError("forward_resistance cannot be negative")
        if voltage < self.forward_voltage:
            return self.shockley_current(voltage, temperature)
        if forward_resistance == 0:
            return math.inf
        return (voltage - self.forward_voltage) / forward_resistance

    def is_forward_biased(self, voltage: float) -> bool:
        """Whether the diode is forward biased (``V > 0``)."""
        return voltage > 0

    def is_in_breakdown(self, voltage: float) -> bool:
        """Whether the reverse voltage exceeds the breakdown rating."""
        if self.breakdown_voltage is None:
            return False
        return voltage <= -self.breakdown_voltage

    def power_dissipation(self, current: float, voltage: float | None = None) -> Quantity:
        """Power dissipated in watts (``P = V·I``).

        If ``voltage`` is omitted the nominal ``forward_voltage`` is used.
        """
        v = self.forward_voltage if voltage is None else voltage
        return Quantity(abs(v * current), WATT)
