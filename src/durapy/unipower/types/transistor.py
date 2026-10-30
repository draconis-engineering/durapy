"""Bipolar junction transistor model for the `UniPower` module."""

from __future__ import annotations

from dataclasses import dataclass

from ...shared.numval_types import Quantity
from ...shared.units import WATT


@dataclass(frozen=True)
class Transistor:
    """A simple large-signal BJT model (active region, forward-active).

    Parameters
    ----------
    beta:
        Forward current gain ``hFE`` (Ic / Ib).
    vbe_on:
        Base-emitter turn-on voltage in volts.
    vce_sat:
        Collector-emitter saturation voltage in volts.
    polarity:
        Either ``"npn"`` or ``"pnp"``.
    max_collector_current:
        Maximum collector current in amperes. Optional.
    max_power:
        Maximum power dissipation in watts. Optional.
    """

    beta: float = 100.0
    vbe_on: float = 0.7
    vce_sat: float = 0.2
    polarity: str = "npn"
    max_collector_current: float | None = None
    max_power: float | None = None

    def __post_init__(self) -> None:
        if self.beta <= 0:
            raise ValueError("beta must be positive")
        if self.vbe_on < 0:
            raise ValueError("vbe_on cannot be negative")
        if self.vce_sat < 0:
            raise ValueError("vce_sat cannot be negative")
        if self.polarity not in ("npn", "pnp"):
            raise ValueError("polarity must be 'npn' or 'pnp'")

    def collector_current(self, base_current: float) -> float:
        """Collector current from the base current (``Ic = β·Ib``)."""
        return self.beta * base_current

    def base_current(self, collector_current: float) -> float:
        """Base current required for a given collector current (``Ib = Ic / β``)."""
        return collector_current / self.beta

    def emitter_current(self, base_current: float) -> float:
        """Emitter current from the base current (``Ie = (β + 1)·Ib``)."""
        return (self.beta + 1) * base_current

    def is_saturated(self, vce: float) -> bool:
        """Whether the device is in saturation for the given ``vce``."""
        return abs(vce) <= self.vce_sat

    def power_dissipation(self, vce: float, collector_current: float) -> Quantity:
        """Power dissipated in watts (``P = Vce·Ic``)."""
        return Quantity(abs(vce * collector_current), WATT)

    def is_within_ratings(self, collector_current: float, vce: float) -> bool:
        """Whether both current and power stay within their ratings."""
        if (
            self.max_collector_current is not None
            and abs(collector_current) > self.max_collector_current
        ):
            return False
        return not (
            self.max_power is not None
            and abs(vce * collector_current) > self.max_power
        )
