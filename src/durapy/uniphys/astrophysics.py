"""`UniPhys` astrophysics source"""

import math

from ..shared.constants import EARTH_M, EARTH_R, HUBBLE, PI, UNI_G, C
from ..shared.numval_types import Quantity
from ..shared.units import METER, MPS, NEWTON, SECOND, G


def schwarzschild_radius(M: float) -> Quantity:
    """Schwarzschild Radius of an object with mass `M`"""
    return Quantity((2 * float(UNI_G) * M) / (float(C) ** 2), METER)


def redshift(λobs: float, λrest: float) -> Quantity:
    from ..shared.units import NUMERICAL

    if λrest == 0:
        raise ValueError("Rest wavelength cannot be zero")
    return Quantity((λobs - λrest) / λrest, NUMERICAL)


def orbital_period(semi_major_axis: float, M: float, m: float) -> Quantity:
    return Quantity(
        2 * float(PI) * math.sqrt(semi_major_axis**3 / (float(UNI_G) * (M + m))), SECOND
    )


def orbital_velocity(
    orbital_radius: float = EARTH_R.value, mass: float = EARTH_M.value
) -> Quantity:
    return Quantity(math.sqrt(float(UNI_G) * mass / orbital_radius), MPS)


def escape_velocity(
    radius: float = EARTH_R.value, mass: float = EARTH_M.value
) -> Quantity:
    return Quantity(math.sqrt(2) * float(orbital_velocity(radius, mass)), MPS)


def newtonian_gravitation(mass1: float, mass2: float, distance: float) -> Quantity:
    if distance == 0:
        raise ValueError("Distance cannot be zero")
    return Quantity(float(UNI_G) * mass1 * mass2 / distance**2, NEWTON)


def surface_gravity(mass: float, radius: float) -> Quantity:
    if radius == 0:
        raise ValueError("Radius cannot be zero")
    return Quantity(float(UNI_G) * mass / radius**2, G)


def tsiolkovsky_rocket_equation(
    exhaust_vel: float, initial_mass: float, final_mass: float
) -> Quantity:
    if final_mass > initial_mass:
        return Quantity(0.0, MPS)

    return Quantity((exhaust_vel * math.log(initial_mass / final_mass)), MPS)


def hubbles_law(Distance: float) -> Quantity:
    return Quantity(float(HUBBLE) * Distance, MPS)
