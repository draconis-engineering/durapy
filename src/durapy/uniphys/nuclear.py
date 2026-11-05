"""`UniPhys` nuclear physics source"""

import math

from ..shared.constants import C
from ..shared.numval_types import Quantity
from ..shared.units import HERTZ, JOULE, NUMERICAL, SECOND


def radioactive_decay(
    initial_quantity: float, decay_const: float, time: float
) -> Quantity:
    """Returns the remaining quantity of a radioactive substance after a given time, based on its initial quantity and decay constant."""
    return Quantity(initial_quantity * math.exp(-decay_const * time), NUMERICAL)


def half_life(decay_const: float) -> Quantity:
    """Returns the half-life of a radioactive substance based on its decay constant."""
    if decay_const == 0:
        raise ValueError("decay_const cannot be zero")
    return Quantity(math.log(2) / decay_const, SECOND)


def activity(quantity: float, decay_const: float) -> Quantity:
    """Returns the activity of a radioactive substance based on its quantity and decay constant."""
    return Quantity(decay_const * quantity, HERTZ)


def mean_lifetime(decay_const: float) -> Quantity:
    """Returns the mean lifetime of a radioactive substance based on its decay constant."""
    if decay_const == 0:
        raise ValueError("decay_const cannot be zero")
    return Quantity(1 / decay_const, SECOND)


def binding_energy(mass_defect: float) -> Quantity:
    """Returns the binding energy of a nucleus based on the mass defect (E=mc^2)."""
    return Quantity(mass_defect * C.value**2, JOULE)


def mass_defect(proton_mass: float, neutron_mass: float, nucleus_mass: float) -> float:
    """Returns the mass defect of a nucleus based on the mass of its protons, neutrons, and the nucleus itself."""
    return (proton_mass + neutron_mass) - nucleus_mass


def decay_constant(half_life: float) -> Quantity:
    """Returns the decay constant of a radioactive substance based on its half-life."""
    from ..shared.units import INVSEC

    if half_life == 0:
        raise ValueError("half_life cannot be zero")
    return Quantity(math.log(2) / half_life, INVSEC)


def decay_rate(initial_quantity: float, decay_const: float) -> Quantity:
    """Returns the decay rate of a radioactive substance based on its initial quantity and decay constant."""
    return Quantity(decay_const * initial_quantity, HERTZ)


def decay_energy(mass_defect: float) -> Quantity:
    """Returns the energy released in a nuclear decay based on the mass defect (E=mc^2)."""
    return Quantity(mass_defect * C.value**2, JOULE)


__all__ = [
    "activity",
    "binding_energy",
    "decay_constant",
    "decay_energy",
    "decay_rate",
    "half_life",
    "mass_defect",
    "mean_lifetime",
    "radioactive_decay",
]
