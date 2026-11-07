"""`UniPhys` orbital mechanics source"""

import math

from ...shared.constants import EARTH_M, EARTH_R, PI, UNI_G
from ...shared.numval_types import Quantity
from ...shared.units import METER, SECOND

_MPS = METER / SECOND


def orbital_period(semi_major_axis: float, *, M: float, m: float) -> Quantity:
    """Orbital period in seconds based on the semi-major axis, the satellite mass (m) and the ... mass (M)"""

    return Quantity(
        2 * PI.value * math.sqrt(semi_major_axis**3 / (UNI_G.value * (M + m))),
        SECOND,
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


__all__ = ["escape_velocity", "orbital_period", "orbital_velocity"]
