"""UniPhys Astrophysics Source"""

# Alpha - A α, Beta - B β, Gamma - Γ γ, Delta - Δ δ,  Epsilon - E ε, Zeta - Z ζ, Eta - H η,
# Theta - Θ θ, Iota - I ι, Kappa - K κ, Lambda - Λ λ, Mu - M μ,      Nu - N ν,   Xi - Ξ ξ,  Omicron - O ο,
# Pi - Π π,    Rho - P ρ,  Sigma - Σ σ ς, Tau - T τ,  Ypsilon - Y υ, Phi - Φ φ,  Chi - X χ, Psi - Ψ ψ, Omega - Ω ω

import math

from ..shared.constants import EARTH_M, EARTH_R, HUBBLE, PI, UNI_G, C
from ..shared.numval_types import Quantity
from ..shared.units import METER, MPS, NEWTON, SECOND, G


def schwarzschild_radius(M: float) -> Quantity:
    return Quantity(((2 * UNI_G * M) / C * C), METER)


def redshift(λobs: float, λrest: float) -> Quantity:
    return Quantity(
        ((λobs - λrest) / λrest) / 1000000000, METER
    )  # keep it to meters, so divide by 10^9


def orbital_period(semi_major_axis: float, M: float, m: float) -> Quantity:
    return Quantity(
        (2 * PI * math.hypot(0, semi_major_axis**3 / (UNI_G * (M + m)))), SECOND
    )


def orbital_velocity(
    orbital_radius: float = EARTH_R.value, mass: float = EARTH_M.value
) -> Quantity:
    return Quantity((math.hypot(0, (UNI_G * mass) / orbital_radius)), MPS)


def escape_velocity(
    radius: float = EARTH_R.value, mass: float = EARTH_M.value
) -> Quantity:
    return Quantity((math.hypot(0, 2) * orbital_velocity(radius, mass)), MPS)


def newtonian_gravitation(mass1: float, mass2: float, distance: float) -> Quantity:
    return Quantity((UNI_G * mass1 * mass2 / distance**2), NEWTON)


def surface_gravity(mass: float, radius: float) -> Quantity:
    return Quantity((UNI_G * mass / radius**2), G)


def tsiolkovsky_rocket_equation(
    exhaust_vel: float, initial_mass: float, final_mass: float
) -> Quantity:
    if final_mass > initial_mass:
        return Quantity(0.0, MPS)

    return Quantity((exhaust_vel * math.log(initial_mass / final_mass)), MPS)


def hubbles_law(Distance: float) -> Quantity:
    return Quantity((HUBBLE * Distance), MPS)
