"""`UniPhys` acoustics source"""

import math

from ..shared.constants import GAS_CONSTANT, MACH
from ..shared.numval_types import Quantity
from ..shared.units import DECIBEL, HERTZ, METER, SECOND


def sound_speed(temp: float, γ: float = 1.4, molar_mass: float = 0.02897) -> Quantity:
    """Calculate the speed of sound in a gas given the temperature, adiabatic index (gamma), and molar mass."""
    return Quantity(math.sqrt((γ * GAS_CONSTANT * temp) / molar_mass), METER / SECOND)


def sound_pressure_level(
    pressure: float, reference_pressure: float = 20e-6
) -> Quantity:
    """Calculate the sound pressure level (SPL) in decibels (dB) given the pressure and reference pressure."""
    return Quantity(20 * math.log10(pressure / reference_pressure), DECIBEL)


def intensity_level(intensity: float, reference_intensity: float = 1e-12) -> Quantity:
    """Calculate the intensity level in decibels (dB) given the intensity and reference intensity."""
    return Quantity(10 * math.log10(intensity / reference_intensity), DECIBEL)


def frequency_from_wavelength(
    wavelength: float, speed_of_sound: float | Quantity = MACH
) -> Quantity:
    """Calculate the frequency of a sound wave given its wavelength and the speed of sound."""
    return Quantity(speed_of_sound / wavelength, HERTZ)


def wavelength_from_frequency(
    freq: float, speed_of_sound: float | Quantity = MACH
) -> Quantity:
    """Calculate the wavelength of a sound wave given its frequency and speed of sound."""
    return Quantity(speed_of_sound / freq, METER)


def decibel_to_intensity(decibel: float, reference_intensity: float = 1e-12) -> float:
    """Convert a sound level in decibels (dB) to intensity given a reference intensity."""
    return reference_intensity * (10 ** (decibel / 10))


def decibel_to_pressure(decibel: float, reference_pressure: float = 20e-6) -> float:
    """Convert a sound level in decibels (dB) to pressure given a reference pressure."""
    return reference_pressure * (10 ** (decibel / 20))


def intensity_to_decibel(intensity: float, reference_intensity: float = 1e-12) -> float:
    """Convert an intensity to decibels (dB) given a reference intensity."""
    return 10 * math.log10(intensity / reference_intensity)


def pressure_to_decibel(pressure: float, reference_pressure: float = 20e-6) -> float:
    """Convert a pressure to decibels (dB) given a reference pressure."""
    return 20 * math.log10(pressure / reference_pressure)


def sound_intensity(
    pressure: float, speed_of_sound: float = MACH.value, density: float = 1.225
) -> float:
    """Calculate the sound intensity given the pressure, speed of sound, and density of the medium."""
    return (pressure**2) / (speed_of_sound * density)


def sound_pressure(
    intensity: float, speed_of_sound: float = MACH.value, density: float = 1.225
) -> float:
    """Calculate the sound pressure given the intensity, speed of sound, and density of the medium."""
    return math.sqrt(intensity * speed_of_sound * density)
