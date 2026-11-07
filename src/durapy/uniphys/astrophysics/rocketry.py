"""`UniPhys` rocketry source"""

import math

from ...shared.constants import C
from ...shared.numval_types import Quantity
from ...shared.units import METER, SECOND

_MPS = METER / SECOND


def tsiolkovsky_rocket_equation(
    *, exhaust_vel: float, initial_mass: float, final_mass: float
) -> Quantity:
    """The Tsiolkovsky rocket equation

    Calculate the delta-V in meters per second for a rocket based on its exhaust velocity, initial (wet) mass and final (dry) mass"""

    if exhaust_vel >= C.value:
        raise ValueError("Exhaust velocity is relativistic")

    if exhaust_vel < 0:
        raise ValueError("Exhaust velocity can't be negative")

    if final_mass > initial_mass:
        return Quantity(0.0, _MPS)

    return Quantity(exhaust_vel * math.log(initial_mass / final_mass), _MPS)


__all__ = ["tsiolkovsky_rocket_equation"]
