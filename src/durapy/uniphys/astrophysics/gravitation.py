"""`UniPhys` gravitation source"""

from ...shared.constants import UNI_G, C
from ...shared.numval_types import Quantity
from ...shared.units import METER, NEWTON, G


def schwarzschild_radius(mass: float) -> Quantity:
    """Schwarzschild Radius of an object from its mass"""

    if mass <= 0:
        raise ValueError("Mass must be greater than zero")
    return Quantity((2 * UNI_G.value * mass) / (C.value**2), METER)


def newtonian_gravitation(distance: float, *, mass1: float, mass2: float) -> Quantity:
    """Newtonian gravitation based on the distance between two bodies and their masses"""

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


__all__ = ["newtonian_gravitation", "schwarzschild_radius", "surface_gravity"]
