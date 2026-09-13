"""`UniPhys` classical mechanics source"""

from ..shared.color_system import color_text
from ..shared.constants import EARTH_G, PI, C
from ..shared.numval_types import Quantity
from ..shared.units import DEGREE, JOULE, NEWTONMETER, RADIAN


def torque(moment_arm_distance: float, force: float) -> Quantity:
    """Returns a `torque` quantity in newtonmeters from moment arm distance in meters and force in newtons."""
    return Quantity((moment_arm_distance * force), NEWTONMETER)


def gear_ratio(driving_teeth: int, driven_teeth: int) -> str:
    """Returns the gear ratio from the driving gear's teeth count and the driven gear's teeth count."""
    if driving_teeth == 0:
        raise ValueError("driving_teeth cannot be zero")
    ratio = driven_teeth / driving_teeth
    if ratio > 1:
        return f"{ratio} - {color_text('Speed-', 'red')} - {color_text('Torque+', 'green')}"
    elif ratio < 1:
        return f"{ratio} - {color_text('Speed+', 'green')} - {color_text('Torque-', 'red')}"
    else:
        return f"{ratio} - Same Speed - Same Torque"


def angular_velocity_r(RPM: float) -> Quantity:
    """Returns angular velocity from RPM in radians/s ( ω = RPM * 2π / 60 )"""
    return Quantity(RPM * float(PI) * 2 / 60, RADIAN)


def angular_velocity_d(RPM: float) -> Quantity:
    """Returns angular velocity from RPM in degrees/s ( 360 deg per revolution )"""
    return Quantity(RPM * 360 / 60, DEGREE)


def kinetic_energy(mass: float, vel: float) -> Quantity:
    """Returns the kinetic energy from mass in kgs and velocity in m/s"""
    return Quantity((0.5 * mass * vel**2), JOULE)


def potential_energy(mass: float, height: float, g: float = EARTH_G.value) -> Quantity:
    """Returns the potential energy of a mass. Gravity is defaulted to 9.8m /s^2"""
    return Quantity(mass * g * height, JOULE)


def einstein_mass_energy_equivalence(mass: float) -> Quantity:
    return Quantity(mass * float(C) ** 2, JOULE)
