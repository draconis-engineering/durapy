"""The `DuraPy` `UniFlight` module provides a collection of functions and classes for performing calculations and simulations related to flight dynamics, aerodynamics, and propulsion."""

from ..shared.color_system import color_text
from ..shared.constants import MACH
from ..shared.numval_types import Quantity
from ..shared.units import NEWTON, PASCAL


def tw_ratio(thrust: float, weight: float) -> str:
    """Thrust to Weight ratio calculator. Ensure consistent units!"""
    ratio = thrust / weight
    return f"Ratio: {color_text(f'{ratio}', 'green' if ratio > 1 else 'red' if ratio != 1 else 'yellow')}"


def mach_number(vel: float, mach: float = MACH.quantity._value.real) -> str:
    """Mach Number Calulator. Speed of sound is defaulted to 343 m/s. Ensure consistent units!"""
    ratio = vel / mach
    label = (
        "SUBSONIC"
        if ratio < 1
        else "TRANSONIC"
        if abs(ratio - 1) < 0.01
        else "SUPERSONIC"
        if ratio < 5
        else "HYPERSONIC"
        if ratio < 10
        else "HIGH-HYPERSONIC"
    )
    color = (
        "red"
        if ratio < 1
        else "yellow"
        if ratio == 1
        else "green"
        if ratio < 5
        else "blue"
        if ratio < 10
        else "violet"
    )
    return f"Ratio: {color_text(f'{ratio} - {label}', color)}"


def dynamic_pressure(velocity: float, air_density: float = 1.225) -> Quantity:
    """Returns the dynamic pressure in Pascals."""
    return Quantity(0.5 * velocity**2 * air_density, PASCAL)


def lift_drag_equation(
    coeff: float, dynamic_pressure: float, ref_area: float
) -> Quantity:
    """Lift/Drag equation calculator. Returns the lift/drag force in Newtons."""
    return Quantity(coeff * dynamic_pressure * ref_area, NEWTON)
