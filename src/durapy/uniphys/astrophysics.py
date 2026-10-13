"""`UniPhys` astrophysics source"""

import math

from ..shared.constants import EARTH_M, EARTH_R, HUBBLE, PI, UNI_G, C
from ..shared.numval_types import Quantity
from ..shared.units import METER, MPS, NEWTON, SECOND, G


def schwarzschild_radius(m: float) -> Quantity:
    """Schwarzschild Radius of an object with mass `m`"""
    if m <= 0:
        raise ValueError("Mass must be greater than zero")
    return Quantity((2 * UNI_G.value * m) / (float(C) ** 2), METER)


def redshift(λobs: float, λrest: float) -> Quantity:
    from ..shared.units import NUMERICAL

    if λrest == 0:
        raise ValueError("Rest wavelength cannot be zero")
    return Quantity((λobs - λrest) / λrest, NUMERICAL)


def orbital_period(semi_major_axis: float, M: float, m: float) -> Quantity:
    return Quantity(
        2 * PI.value * math.sqrt(semi_major_axis**3 / (UNI_G.value * (M + m))), SECOND
    )


def orbital_velocity(
    orbital_radius: float = EARTH_R.value, mass: float = EARTH_M.value
) -> Quantity:
    return Quantity(math.sqrt(UNI_G.value * mass / orbital_radius), MPS)


def escape_velocity(
    radius: float = EARTH_R.value, mass: float = EARTH_M.value
) -> Quantity:
    if radius <= 0 or mass <= 0:
        raise ValueError("Radius and mass must be greater than zero")
    return Quantity(math.sqrt(2) * float(orbital_velocity(radius, mass)), MPS)


def newtonian_gravitation(mass1: float, mass2: float, distance: float) -> Quantity:
    if distance <= 0:
        raise ValueError("Distance must be greater than zero")
    if mass1 <= 0 or mass2 <= 0:
        raise ValueError("Masses must be greater than zero")
    return Quantity(UNI_G.value * mass1 * mass2 / distance**2, NEWTON)


def surface_gravity(mass: float, radius: float) -> Quantity:
    if radius <= 0 or mass <= 0:
        raise ValueError("Radius and mass must be greater than zero")
    return Quantity(UNI_G.value * mass / radius**2, G)


def tsiolkovsky_rocket_equation(
    exhaust_vel: float, initial_mass: float, final_mass: float
) -> Quantity:

    if exhaust_vel >= C.value:
        raise ValueError("Exhaust velocity is relativistic")

    if final_mass > initial_mass:
        return Quantity(0.0, MPS)

    return Quantity((exhaust_vel * math.log(initial_mass / final_mass)), MPS)


def hubbles_law(distance: float) -> Quantity:
    if distance <= 0:
        raise ValueError("Distance must be greater than zero")
    return Quantity(float(HUBBLE) * distance, MPS)
