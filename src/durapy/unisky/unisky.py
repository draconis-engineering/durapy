"""`UniSky` source"""

from ..shared.color_system import color_text
from ..shared.constants import EARTH_G, GAS_CONSTANT, MACH
from ..shared.numval_types import Quantity
from ..shared.units import NEWTON
from ..uniphys.fluid_dynamics import (
    bernoullis_equation,
    dynamic_pressure,
)
from ..uniphys.fluid_dynamics import (
    reynolds_number as _reynolds_number,
)
from ..uniphys.thermodynamics import ideal_gas_law as _ideal_gas_law


def tw_ratio(thrust: float, weight: float) -> str:
    """Thrust to Weight ratio calculator. Ensure consistent units!"""
    ratio = thrust / weight
    return f"Ratio: {color_text(f'{ratio}', 'green' if ratio > 1 else 'red' if ratio != 1 else 'yellow')}"


def mach_number(vel: float, mach: float = MACH.value) -> str:
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


def lift_drag_equation(
    coeff: float, dynamic_pressure: float, ref_area: float
) -> Quantity:
    """Lift/Drag equation calculator. Returns the lift/drag force in Newtons."""
    return Quantity(coeff * dynamic_pressure * ref_area, NEWTON)


def reynolds_number(
    velocity: float, chord_length: float, kinematic_viscosity: float
) -> float:
    """Calculates the dimensionless Reynolds Number to predict flow patterns.

    Thin wrapper over :func:`durapy.uniphys.fluid_dynamics.reynolds_number` that
    keeps the aerospace-style ``chord_length`` parameter name.
    """
    return _reynolds_number(velocity, chord_length, kinematic_viscosity)


def aspect_ratio(wingspan: float, wing_area: float) -> float:
    """Calculates the wing aspect ratio (Span^2 / Area)."""
    return (wingspan**2) / wing_area


def wing_loading(weight_force: float, wing_area: float) -> float:
    """Calculates wing loading (Force per unit area)."""
    return weight_force / wing_area


def glide_ratio(lift: float, drag: float) -> float:
    """Calculates the glide ratio (L/D ratio)."""
    return lift / drag


def specific_impulse_by_thrust(
    thrust: float, fuel_mass_flow_rate: float, g0: float = EARTH_G.value
) -> float:
    """Calculates specific impulse (Isp) in seconds using thrust and mass flow rate."""
    return thrust / (fuel_mass_flow_rate * g0)


def rocket_thrust_equation(
    *, mdot: float, v_e: float, p_e: float, p_a: float, a_e: float
) -> float:
    """Calculates the thrust of a rocket based on
    fuel mass flow rate (``mdot``), effective exhaust velocity (``v_e``),
    exit pressure (``p_e``), ambient pressure (``p_a``) and nozzle exit area (``a_e``)"""
    return mdot * v_e + (p_e - p_a) * a_e


def ideal_gas_law(
    *,
    P: float | None = None,
    V: float | None = None,
    n: float | None = None,
    R: float = GAS_CONSTANT.value,
    T: float | None = None,
) -> str:
    """Solve for the ideal gas law and return the solved variable as a string.

    Thin wrapper over :func:`durapy.uniphys.thermodynamics.ideal_gas_law` that
    preserves UniSky's string return format.

    Variables
    ---------
    • P – Absolute pressure (measured in pascals [Pa] or atmospheres [atm])
    • V – Volume of the gas (measured in cubic meters [m³] or liters [L])
    • n – Amount of substance in moles
    • R – Universal gas constant
    • T – Absolute temperature (measured in Kelvin [K])"""

    solved = _ideal_gas_law(P=P, V=V, n=n, T=T, R=R)
    values: dict[str, float] = dict(zip(("P", "V", "n", "T"), solved))
    missing = next(
        key for key, value in {"P": P, "V": V, "n": n, "T": T}.items() if value is None
    )

    return f"{missing} = {values[missing]}"


__all__ = [
    "aspect_ratio",
    "bernoullis_equation",
    "dynamic_pressure",
    "glide_ratio",
    "ideal_gas_law",
    "lift_drag_equation",
    "mach_number",
    "reynolds_number",
    "rocket_thrust_equation",
    "specific_impulse_by_thrust",
    "tw_ratio",
    "wing_loading",
]
