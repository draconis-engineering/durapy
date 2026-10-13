"""Signal oscillator model for the `UniPower` module."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ...shared.numval_types import Quantity
from ...shared.units import HERTZ, SECOND

WAVEFORMS = ("sine", "square", "triangle", "sawtooth")


@dataclass(frozen=True)
class Oscillator:
    """A periodic signal source.

    Parameters
    ----------
    frequency:
        Output frequency in hertz (Hz).
    amplitude:
        Peak amplitude (in the unit implied by the caller).
    waveform:
        One of ``"sine"``, ``"square"``, ``"triangle"`` or ``"sawtooth"``.
    """

    frequency: float
    amplitude: float = 1.0
    waveform: str = "sine"

    def __post_init__(self) -> None:
        if self.frequency <= 0:
            raise ValueError("frequency must be positive")
        if self.waveform not in WAVEFORMS:
            raise ValueError(f"waveform must be one of {WAVEFORMS}")

    def period(self) -> Quantity:
        """Period in seconds (T = 1 / f)."""
        return Quantity(1 / self.frequency, SECOND)

    def angular_frequency(self) -> Quantity:
        """Angular frequency in hertz-equivalent (ω = 2π·f)."""
        return Quantity(2 * math.pi * self.frequency, HERTZ)

    def value_at(self, time: float) -> float:
        """Instantaneous signal value at ``time`` seconds."""
        phase = (self.frequency * time) % 1.0
        angle = 2 * math.pi * phase
        if self.waveform == "sine":
            return self.amplitude * math.sin(angle)
        if self.waveform == "square":
            return self.amplitude * (1.0 if phase < 0.5 else -1.0)
        if self.waveform == "triangle":
            return self.amplitude * (2 / math.pi) * math.asin(math.sin(angle))
        # sawtooth: ramps from -A to +A over one period
        return self.amplitude * (2 * phase - 1)
