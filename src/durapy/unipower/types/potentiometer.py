"""Potentiometer model for the `UniPower` module."""

from __future__ import annotations

from dataclasses import dataclass

from ...shared.numval_types import Quantity
from ...shared.units import OHM, VOLT


@dataclass(frozen=True)
class Potentiometer:
    """A three-terminal variable resistor (rheostat/divider).

    The wiper splits the track into two resistances. ``position`` runs from 0
    (wiper at the bottom terminal) to 1 (wiper at the top terminal).

    Parameters
    ----------
    total_resistance:
        End-to-end track resistance in ohms (Ω).
    position:
        Wiper position in the closed interval ``[0, 1]``.
    """

    total_resistance: float
    position: float = 0.0

    def __post_init__(self) -> None:
        if self.total_resistance <= 0:
            raise ValueError("total_resistance must be positive")
        if not 0 <= self.position <= 1:
            raise ValueError("position must be between 0 and 1")

    def bottom_resistance(self) -> Quantity:
        """Resistance between the bottom terminal and the wiper."""
        return Quantity(self.position * self.total_resistance, OHM)

    def top_resistance(self) -> Quantity:
        """Resistance between the wiper and the top terminal."""
        return Quantity((1 - self.position) * self.total_resistance, OHM)

    def resistances(self) -> tuple[Quantity, Quantity]:
        """Both track halves as ``(bottom, top)`` resistances."""
        return self.bottom_resistance(), self.top_resistance()

    def wiper_voltage(self, v_bottom: float, v_top: float) -> Quantity:
        """Wiper voltage for a fixed potential across the track.

        ``position=0`` gives ``v_bottom`` and ``position=1`` gives ``v_top``.
        """
        return Quantity(v_bottom + self.position * (v_top - v_bottom), VOLT)
