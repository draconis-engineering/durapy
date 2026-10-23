"""`UniSky` source"""

import sympy as sp

from ..shared.color_system import color_text
from ..shared.constants import EARTH_G, GAS_CONSTANT, MACH
from ..shared.numval_types import Quantity
from ..shared.units import NEWTON, PASCAL


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


def dynamic_pressure(velocity: float, air_density: float = 1.225) -> Quantity:
    """Returns the dynamic pressure in Pascals."""
    return Quantity(0.5 * velocity**2 * air_density, PASCAL)


def lift_drag_equation(
    coeff: float, dynamic_pressure: float, ref_area: float
) -> Quantity:
    """Lift/Drag equation calculator. Returns the lift/drag force in Newtons."""
    return Quantity(coeff * dynamic_pressure * ref_area, NEWTON)


def reynolds_number(
    velocity: float, chord_length: float, kinematic_viscosity: float
) -> float:
    """Calculates the dimensionless Reynolds Number to predict flow patterns."""
    return (velocity * chord_length) / kinematic_viscosity


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


def bernoullis_equation(
    *,
    P1: float | None = None,
    v1: float | None = None,
    h1: float | None = None,
    P2: float | None = None,
    v2: float | None = None,
    h2: float | None = None,
    rho: float = 1000,
    g: float = 9.81,
) -> str:
    """Solve for Bernoullis Equation with exactly ONE missing variable.

    The equation is valid only when specific conditions are met:
    • Steady flow: Fluid properties at a point do not change over time.
    • Incompressible flow: Density remains constant (true for liquids and low-speed gases).
    • Inviscid flow: Friction and viscosity have a negligible effect.
    • Streamline flow: Fluid flows along smooth, continuous paths without turbulence or heat addition."""

    p1_s, v1_s, h1_s, p2_s, v2_s, h2_s, rho_s, g_s = sp.symbols(
        "P1 v1 h1 P2 v2 h2 rho g"
    )

    # Define the equation: LHS - RHS = 0
    eq = (p1_s + 0.5 * rho_s * v1_s**2 + rho_s * g_s * h1_s) - (
        p2_s + 0.5 * rho_s * v2_s**2 + rho_s * g_s * h2_s
    )

    # Map inputs to symbols
    inputs = {
        p1_s: P1,
        v1_s: v1,
        h1_s: h1,
        p2_s: P2,
        v2_s: v2,
        h2_s: h2,
        rho_s: rho,
        g_s: g,
    }

    # Filter out the variable that is missing (None)
    missing = [k for k, v in inputs.items() if v is None]
    knowns = {k: v for k, v in inputs.items() if v is not None}

    if len(missing) != 1:
        raise ValueError(
            f"Provide exactly 5 of the main variables. Missing: {[m.name for m in missing]}"
        )

    # Substitute known values into equation and solve
    substituted_eq = eq.subs(knowns)
    solution = sp.solve(substituted_eq, missing[0])

    return f"{missing[0].name} = {solution[0]}"


def ideal_gas_law(
    *,
    P: float | None = None,
    V: float | None = None,
    n: float | None = None,
    R: float = GAS_CONSTANT.value,
    T: float | None = None,
) -> str:
    """Solve for the ideal gas law

    Variables
    ---------
    • P – Absolute pressure (measured in pascals [Pa] or atmospheres [atm])
    • V – Volume of the gas (measured in cubic meters [m³] or liters [L])
    • n – Amount of substance in moles
    • R – Universal gas constant
    • T – Absolute temperature (measured in Kelvin [K]"""

    p_s, v_s, n_s, r_s, t_s = sp.symbols("P V n R T")

    # Define the equation: LHS - RHS = 0
    eq = p_s * v_s - n_s * r_s * t_s

    # Map inputs to symbols
    inputs = {p_s: P, v_s: V, n_s: n, r_s: R, t_s: T}

    # Filter out the variable that is missing (None)
    missing = [k for k, v in inputs.items() if v is None]
    knowns = {k: v for k, v in inputs.items() if v is not None}

    if len(missing) != 1:
        raise ValueError(
            f"Provide exactly 5 of the main variables. Missing: {[m.name for m in missing]}"
        )

    # Substitute known values into equation and solve
    substituted_eq = eq.subs(knowns)
    solution = sp.solve(substituted_eq, missing[0])

    return f"{missing[0].name} = {solution[0]}"


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
