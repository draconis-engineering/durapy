"""
The UniPhys function and class library for `DuraPy`.
This library contains functions and classes for physics calculations and simulations.
The functions are designed to be easy to use and understand, with clear input and output formats.
The library is still in development and may contain some unstable functions that are not yet fully tested.
"""

from . import (
    acoustics,
    astrophysics,
    electromagnetics,
    fluid_dynamics,
    mechanics,
    nuclear,
    quantum,
    thermodynamics,
)

__all__ = [
    "acoustics",
    "astrophysics",
    "electromagnetics",
    "fluid_dynamics",
    "mechanics",
    "nuclear",
    "quantum",
    "thermodynamics",
]
