"""
The UniPower function library for the `DuraPy` library.
This library contains functions for electrical calculations and simulations. The functions are designed to be easy to use and understand, with clear input and output formats.
The library is still in development and may contain some unstable functions that are not yet fully tested.
"""

from .types.capacitor import Capacitor
from .types.circuit import Circuit
from .types.diode import Diode
from .types.fuse import Fuse
from .types.ic import IC
from .types.inductor import Inductor
from .types.oscillator import Oscillator
from .types.potentiometer import Potentiometer
from .types.resistor import BANDS, MULTIPLIERS, TOLERANCES, Resistor
from .types.transistor import Transistor
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
    "BANDS",
    "IC",
    "MULTIPLIERS",
    "TOLERANCES",
    "Capacitor",
    "Circuit",
    "Diode",
    "Fuse",
    "Inductor",
    "Oscillator",
    "Potentiometer",
    "Resistor",
    "Transistor",
    "inductor_impedance",
    "ohms_law",
    "power_dissipation",
    "rc_time_constant",
    "total_capacitance",
    "total_esr",
    "volt_divider",
]
