"""AC and RLC analysis helpers for the `UniPower` module.

This module collects steady-state (sinusoidal) analysis tools: reactance and
impedance, resonance, quality factor, RMS, decibels and power relationships.
All ``*_reactance``/``*_impedance`` functions take frequencies in hertz and
return SI quantities.
"""

from __future__ import annotations

import cmath
import math
from collections.abc import Iterable

from ..shared.constants import PI
from ..shared.numval_types import Quantity
from ..shared.units import FARAD, HENRY, HERTZ, OHM, WATT

__all__ = [
    "apparent_power",
    "bandwidth",
    "capacitive_reactance",
    "cutoff_frequency_rc",
    "cutoff_frequency_rl",
    "dbm_to_watts",
    "decibels_amplitude",
    "decibels_power",
    "from_decibels",
    "high_pass_magnitude",
    "impedance_magnitude_phase",
    "impedance_rlc",
    "inductive_reactance",
    "low_pass_magnitude",
    "parallel_capacitance",
    "parallel_inductance",
    "parallel_quality_factor",
    "parallel_resistance",
    "power_factor",
    "reactive_power",
    "real_power",
    "resonant_frequency",
    "rms",
    "rms_from_peak",
    "series_capacitance",
    "series_inductance",
    "series_quality_factor",
    "series_resistance",
    "watts_to_dbm",
]


def req_pos(name: str, value: float) -> None:
    """Require positive number"""
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def req_non_zero(name: str, value: float) -> None:
    """Require non-negative number"""
    if value < 0:
        raise ValueError(f"{name} cannot be negative")


# --------------------------------------------------------------------------- #
# Series / parallel combinations
# --------------------------------------------------------------------------- #


def series_resistance(*resistances: float) -> Quantity:
    """Equivalent resistance of resistors in series (sum, in ohms)."""
    if not resistances:
        raise ValueError("at least one resistance is required")
    for r in resistances:
        req_non_zero("resistance", r)
    return Quantity(math.fsum(resistances), OHM)


def parallel_resistance(*resistances: float) -> Quantity:
    """Equivalent resistance of resistors in parallel (harmonics, in ohms)."""
    if not resistances:
        raise ValueError("at least one resistance is required")
    for r in resistances:
        req_non_zero("resistance", r)
    if any(r == 0 for r in resistances):
        return Quantity(0.0, OHM)
    return Quantity(1 / math.fsum(1 / r for r in resistances), OHM)


def series_capacitance(*capacitances: float) -> Quantity:
    """Equivalent capacitance of capacitors in series (in farads)."""
    if not capacitances:
        raise ValueError("at least one capacitance is required")
    for c in capacitances:
        req_pos("capacitance", c)
    return Quantity(1 / math.fsum(1 / c for c in capacitances), FARAD)


def parallel_capacitance(*capacitances: float) -> Quantity:
    """Equivalent capacitance of capacitors in parallel (in farads)."""
    if not capacitances:
        raise ValueError("at least one capacitance is required")
    for c in capacitances:
        req_pos("capacitance", c)
    return Quantity(math.fsum(capacitances), FARAD)


def series_inductance(*inductances: float) -> Quantity:
    """Equivalent inductance of inductors in series (in henrys)."""
    if not inductances:
        raise ValueError("at least one inductance is required")
    for l in inductances:
        req_pos("inductance", l)
    return Quantity(math.fsum(inductances), HENRY)


def parallel_inductance(*inductances: float) -> Quantity:
    """Equivalent inductance of inductors in parallel (in henrys)."""
    if not inductances:
        raise ValueError("at least one inductance is required")
    for l in inductances:
        req_pos("inductance", l)
    return Quantity(1 / math.fsum(1 / l for l in inductances), HENRY)


# --------------------------------------------------------------------------- #
# Reactance and impedance
# --------------------------------------------------------------------------- #


def capacitive_reactance(frequency: float, capacitance: float) -> Quantity:
    """Capacitive reactance ``Xc = 1 / (2π·f·C)`` in ohms."""
    req_pos("frequency", frequency)
    req_pos("capacitance", capacitance)
    return Quantity(1 / (2 * PI * frequency * capacitance), OHM)


def inductive_reactance(frequency: float, inductance: float) -> Quantity:
    """Inductive reactance ``Xʟ = 2π·f·L`` in ohms."""
    req_pos("frequency", frequency)
    req_pos("inductance", inductance)
    return Quantity(2 * PI * frequency * inductance, OHM)


def impedance_rlc(
    frequency: float,
    resistance: float,
    inductance: float = 0.0,
    capacitance: float | None = None,
) -> complex:
    """Series RLC impedance ``Z = R + j(ωL - 1/(ωC))`` in ohms.

    Pass ``capacitance=None`` to omit the capacitive term.
    """
    req_pos("frequency", frequency)
    req_non_zero("resistance", resistance)
    req_non_zero("inductance", inductance)
    omega = 2 * PI.value * frequency
    reactance = omega * inductance
    if capacitance is not None:
        req_pos("capacitance", capacitance)
        reactance -= 1 / (omega * capacitance)
    return complex(resistance, reactance)


def impedance_magnitude_phase(impedance: complex) -> tuple[float, float]:
    """Return ``(|Z|, phase)`` where phase is in degrees in ``(-180, 180]``."""
    return abs(impedance), math.degrees(cmath.phase(impedance))


# --------------------------------------------------------------------------- #
# Resonance and quality factor
# --------------------------------------------------------------------------- #


def resonant_frequency(inductance: float, capacitance: float) -> Quantity:
    """LC resonant frequency ``f = 1 / (2π·√(L·C))`` in hertz."""
    req_pos("inductance", inductance)
    req_pos("capacitance", capacitance)
    return Quantity(1 / (2 * PI * math.sqrt(inductance * capacitance)), HERTZ)


def series_quality_factor(
    resistance: float, inductance: float, capacitance: float
) -> float:
    """Series RLC quality factor ``Q = (1/R)·√(L/C)``."""
    req_pos("resistance", resistance)
    req_pos("inductance", inductance)
    req_pos("capacitance", capacitance)
    return (1 / resistance) * math.sqrt(inductance / capacitance)


def parallel_quality_factor(
    resistance: float, inductance: float, capacitance: float
) -> float:
    """Parallel RLC quality factor ``Q = R·√(C/L)``."""
    req_pos("resistance", resistance)
    req_pos("inductance", inductance)
    req_pos("capacitance", capacitance)
    return resistance * math.sqrt(capacitance / inductance)


def bandwidth(center_frequency: float, quality_factor: float) -> Quantity:
    """Half-power bandwidth ``BW = f0 / Q`` in hertz."""
    req_pos("center_frequency", center_frequency)
    req_pos("quality_factor", quality_factor)
    return Quantity(center_frequency / quality_factor, HERTZ)


# --------------------------------------------------------------------------- #
# Power
# --------------------------------------------------------------------------- #


def power_factor(phase_angle_degrees: float) -> float:
    """Displacement power factor ``cos(φ)`` from a phase angle in degrees."""
    return math.cos(math.radians(phase_angle_degrees))


def apparent_power(voltage_rms: float, current_rms: float) -> Quantity:
    """Apparent power ``S = Vrms·Irms`` in volt-amperes (reported as watts)."""
    req_non_zero("voltage_rms", voltage_rms)
    req_non_zero("current_rms", current_rms)
    return Quantity(voltage_rms * current_rms, WATT)


def real_power(
    voltage_rms: float, current_rms: float, phase_angle_degrees: float
) -> Quantity:
    """Active power ``P = Vrms·Irms·cos(φ)`` in watts."""
    req_non_zero("voltage_rms", voltage_rms)
    req_non_zero("current_rms", current_rms)
    return Quantity(
        voltage_rms * current_rms * math.cos(math.radians(phase_angle_degrees)), WATT
    )


def reactive_power(
    voltage_rms: float, current_rms: float, phase_angle_degrees: float
) -> Quantity:
    """Reactive power ``Q = Vrms·Irms·sin(φ)`` in volt-amperes reactive."""
    req_non_zero("voltage_rms", voltage_rms)
    req_non_zero("current_rms", current_rms)
    return Quantity(
        voltage_rms * current_rms * math.sin(math.radians(phase_angle_degrees)), WATT
    )


# --------------------------------------------------------------------------- #
# RMS and decibels
# --------------------------------------------------------------------------- #


def rms(values: Iterable[float]) -> float:
    """Root-mean-square of a non-empty sequence of samples."""
    samples = list(values)
    if not samples:
        raise ValueError("rms requires at least one sample")
    return math.sqrt(math.fsum(v * v for v in samples) / len(samples))


def rms_from_peak(peak: float) -> float:
    """RMS of a sinusoid from its peak amplitude (``peak / √2``)."""
    req_non_zero("peak", peak)
    return peak / math.sqrt(2)


def decibels_power(ratio: float) -> float:
    """Power ratio to decibels (``10·log10(ratio)``)."""
    req_pos("ratio", ratio)
    return 10 * math.log10(ratio)


def decibels_amplitude(ratio: float) -> float:
    """Amplitude/voltage ratio to decibels (``20·log10(ratio)``)."""
    req_pos("ratio", ratio)
    return 20 * math.log10(ratio)


def from_decibels(decibel: float, *, amplitude: bool = False) -> float:
    """Convert decibels back to a ratio (power by default)."""
    return 10 ** (decibel / (20 if amplitude else 10))


def dbm_to_watts(power_dbm: float) -> Quantity:
    """Power in dBm to watts (0 dBm = 1 mW)."""
    return Quantity(10 ** (power_dbm / 10) / 1000, WATT)


def watts_to_dbm(power_watts: float) -> float:
    """Power in watts to dBm."""
    req_pos("power_watts", power_watts)
    return 10 * math.log10(power_watts * 1000)


# --------------------------------------------------------------------------- #
# Filter cut-offs
# --------------------------------------------------------------------------- #


def cutoff_frequency_rc(resistance: float, capacitance: float) -> Quantity:
    """-3 dB cut-off of an RC filter ``fc = 1 / (2π·R·C)`` in hertz."""
    req_pos("resistance", resistance)
    req_pos("capacitance", capacitance)
    return Quantity(1 / (2 * PI * resistance * capacitance), HERTZ)


def cutoff_frequency_rl(resistance: float, inductance: float) -> Quantity:
    """-3 dB cut-off of an RL filter ``fc = R / (2π·L)`` in hertz."""
    req_pos("resistance", resistance)
    req_pos("inductance", inductance)
    return Quantity(resistance / (2 * PI * inductance), HERTZ)


def low_pass_magnitude(frequency: float, cutoff_frequency: float) -> float:
    """First-order low-pass gain magnitude at ``frequency``."""
    req_non_zero("frequency", frequency)
    req_pos("cutoff_frequency", cutoff_frequency)
    return 1 / math.sqrt(1 + (frequency / cutoff_frequency) ** 2)


def high_pass_magnitude(frequency: float, cutoff_frequency: float) -> float:
    """First-order high-pass gain magnitude at ``frequency``."""
    req_non_zero("frequency", frequency)
    req_pos("cutoff_frequency", cutoff_frequency)
    ratio = frequency / cutoff_frequency
    return ratio / math.sqrt(1 + ratio**2)
