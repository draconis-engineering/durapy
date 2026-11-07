"""`UniPhys` classical mechanics source"""

from ...shared.color_system import color_text
from ...shared.constants import EARTH_G, PI
from ...shared.numval_types import Quantity
from ...shared.units import DEGREE, JOULE, NEWTONMETER, RADIAN
from ..modern.relativity import einstein_mass_energy_equivalence


def torque(moment_arm_distance: float, force: float) -> Quantity:
    """Returns a `torque` quantity in newtonmeters from moment arm distance in meters and force in newtons."""
    return Quantity((moment_arm_distance * force), NEWTONMETER)


# Pos-only because of the names being easily mixed up
def gear_ratio(*, driving: int, driven: int) -> str:
    """Returns the gear ratio from the driving gear's teeth count and the driven gear's teeth count."""
    if driving == 0:
        raise ValueError("driving_teeth cannot be zero")
    ratio = driven / driving
    if ratio > 1:
        return f"{ratio} - {color_text('Speed-', 'red')} - {color_text('Torque+', 'green')}"
    elif ratio < 1:
        return f"{ratio} - {color_text('Speed+', 'green')} - {color_text('Torque-', 'red')}"
    else:
        return f"{ratio} - Same Speed - Same Torque"


def angular_velocity_radians(rpm: float, /) -> Quantity:
    """Returns angular velocity from RPM in radians/s ( ω = RPM * 2π / 60 )"""
    return Quantity(rpm * PI * 2 / 60, RADIAN)


def angular_velocity_degrees(rpm: float, /) -> Quantity:
    """Returns angular velocity from RPM in degrees/s ( 360 deg per revolution )"""
    return Quantity(rpm * 360 / 60, DEGREE)


def kinetic_energy(mass: float, vel: float) -> Quantity:
    """Returns the kinetic energy from mass in kgs and velocity in m/s"""
    return Quantity(0.5 * mass * vel**2, JOULE)


def potential_energy(
    mass: float, height: float, *, g: float = EARTH_G.value
) -> Quantity:
    """Returns the potential energy of a mass. Gravity is defaulted to 9.8m /s^2"""
    return Quantity(mass * g * height, JOULE)


__all__ = [
    "angular_velocity_degrees",
    "angular_velocity_radians",
    "einstein_mass_energy_equivalence",
    "gear_ratio",
    "kinetic_energy",
    "potential_energy",
    "torque",
]
