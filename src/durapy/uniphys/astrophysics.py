"""`UniPhys` astrophysics source"""

import math

from ..shared.constants import EARTH_M, EARTH_R, HUBBLE, PI, UNI_G, C
from ..shared.numval_types import Quantity
from ..shared.units import METER, SECOND, G

_MPS = METER / SECOND


def schwarzschild_radius(mass: float) -> Quantity:
    """Schwarzschild Radius of an object from its mass"""

    if mass <= 0:
        raise ValueError("Mass must be greater than zero")
    return Quantity((2 * UNI_G.value * mass) / (C.value**2), METER)


def redshift(*, λobs: float, λrest: float) -> Quantity:
    """The redshift of a photon based on the wavelength at rest and the observed wavelength"""
    from ..shared.units import NUMERICAL

    if λrest == 0:
        raise ValueError("Rest wavelength cannot be zero")
    return Quantity((λobs - λrest) / λrest, NUMERICAL)


def orbital_period(semi_major_axis: float, *, M: float, m: float) -> Quantity:
    """Orbital period in seconds based on the semi-major axis, the satellite mass (m) and the ... mass (M)"""

    return Quantity(
        2 * PI.value * math.sqrt(semi_major_axis**3 / (UNI_G.value * (M + m))), SECOND
    )


def orbital_velocity(
    orbital_radius: float = EARTH_R.value, mass: float = EARTH_M.value
) -> Quantity:
    """The orbital velocity for a stellar body based on its mass and the orbital radius"""

    if orbital_radius <= 0 or mass <= 0:
        raise ValueError("Radius and mass must be greater than zero")
    return Quantity(math.sqrt(UNI_G.value * mass / orbital_radius), _MPS)


def escape_velocity(
    radius: float = EARTH_R.value, mass: float = EARTH_M.value
) -> Quantity:
    """The escape velocity for a stellar body based on its radius and mass"""

    if radius <= 0 or mass <= 0:
        raise ValueError("Radius and mass must be greater than zero")
    return Quantity(math.sqrt(2) * orbital_velocity(radius, mass), _MPS)


def newtonian_gravitation(distance: float, *, mass1: float, mass2: float) -> Quantity:
    """Newtonian gravitation based on the distance between two bodies and their masses"""
    from ..shared.units import NEWTON

    if distance <= 0:
        raise ValueError("Distance must be greater than zero")
    if mass1 <= 0 or mass2 <= 0:
        raise ValueError("Masses must be greater than zero")
    return Quantity(UNI_G.value * mass1 * mass2 / distance**2, NEWTON)


def surface_gravity(mass: float, radius: float) -> Quantity:
    """Surface gravity of a stellar body from its mass and the radius (distance from the center)"""

    if radius <= 0 or mass <= 0:
        raise ValueError("Radius and mass must be greater than zero")
    return Quantity(UNI_G.value * mass / radius**2, G)


def tsiolkovsky_rocket_equation(
    *, exhaust_vel: float, initial_mass: float, final_mass: float
) -> Quantity:
    """The Tsiolkovsky rocket equation

    Calculate the delta-V in meters per second for a rocket based on its exhaust velocity, inital (wet) mass and final (dry) mass"""

    # Really fucking fast rocket
    if exhaust_vel >= C.value:
        raise ValueError("Exhaust velocity is relativistic")

    # Really shitty rocket
    if exhaust_vel < 0:
        raise ValueError("Exhaust velocity can't be negative")

    # Strange rocket
    if final_mass > initial_mass:
        return Quantity(0.0, _MPS)

    # Normal rocket
    return Quantity(exhaust_vel * math.log(initial_mass / final_mass), _MPS)


def hubbles_law(distance: float) -> Quantity:
    if distance <= 0:
        raise ValueError("Distance must be greater than zero")
    return Quantity(HUBBLE.value * distance, _MPS)


__all__ = [
    "escape_velocity",
    "hubbles_law",
    "newtonian_gravitation",
    "orbital_period",
    "orbital_velocity",
    "redshift",
    "schwarzschild_radius",
    "surface_gravity",
    "tsiolkovsky_rocket_equation",
]
