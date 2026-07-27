"""
The UniPower function library for the `DuraPy` library.
This library contains functions for electrical calculations and simulations. The functions are designed to be easy to use and understand, with clear input and output formats.
The library is still in development and may contain some unstable functions that are not yet fully tested.
"""

from .types import (
    capacitor,
    diode,
    fuse,
    ic,
    inductor,
    oscillator,
    potentiometer,
    resistor,
    transistor,
)
from .unipower import (
    inductor_impedance,
    ohms_law,
    power_dissipation,
    rc_time_constant,
    total_capacitance,
    total_esr,
    volt_divider,
)

__all__ = [
    "capacitor",
    "diode",
    "fuse",
    "ic",
    "inductor",
    "inductor_impedance",
    "ohms_law",
    "oscillator",
    "potentiometer",
    "power_dissipation",
    "rc_time_constant",
    "resistor",
    "total_capacitance",
    "total_esr",
    "transistor",
    "volt_divider",
]
