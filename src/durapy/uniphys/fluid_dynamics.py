"""`UniPhys` fluid dynamics source"""

import sympy as sp

from ..shared.numval_types import Quantity
from ..shared.units import PASCAL


def reynolds_number(
    velocity: float, characteristic_length: float, kinematic_viscosity: float
) -> float:
    """
    Calculate the Reynolds number for a given flow.

    Parameters
    ----------
    velocity: The velocity of the fluid (m/s).
    characteristic_length: The characteristic length of the flow (m).
    kinematic_viscosity: The kinematic viscosity of the fluid (m^2/s).

    Returns
    -------
    float: The Reynolds number.
    """
    return (velocity * characteristic_length) / kinematic_viscosity


def dynamic_pressure(velocity: float, air_density: float = 1.225) -> Quantity:
    """Returns the dynamic pressure (½ρv²) in Pascals."""
    return Quantity(0.5 * velocity**2 * air_density, PASCAL)


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
            f"Provide exactly 7 of the main variables. Missing: {[m.name for m in missing]}"
        )

    # Substitute known values into equation and solve
    substituted_eq = eq.subs(knowns)
    solution = sp.solve(substituted_eq, missing[0])

    return f"{missing[0].name} = {solution[0]}"
