"""UniPhys Nuclear Physics Source"""

from ..shared.constants import E
from ..shared.numval_types import Quantity
from ..shared.units import NUMERICAL


def radioactive_decay(
    initial_quantity: float, decay_const: float, time: float
) -> Quantity:
    """Returns the remaining quantity of a radioactive substance after a given time, based on its initial quantity and decay constant."""
    return Quantity(
        initial_quantity * (E ** (-decay_const * time)), NUMERICAL
    )  # Not kg?


def half_life(decay_const: float) -> float:
    """Returns the half-life of a radioactive substance based on its decay constant."""
    return 0.693 / decay_const


def activity(quantity: float, decay_const: float) -> float:
    """Returns the activity of a radioactive substance based on its quantity and decay constant."""
    return decay_const * quantity


def mean_lifetime(decay_const: float) -> float:
    """Returns the mean lifetime of a radioactive substance based on its decay constant."""
    return 1 / decay_const


def binding_energy(mass_defect: float) -> Quantity:
    """Returns the binding energy of a nucleus based on the mass defect."""
    return mass_defect * E


def mass_defect(proton_mass: float, neutron_mass: float, nucleus_mass: float) -> float:
    """Returns the mass defect of a nucleus based on the mass of its protons, neutrons, and the nucleus itself."""
    return (proton_mass + neutron_mass) - nucleus_mass


def decay_constant(half_life: float) -> float:
    """Returns the decay constant of a radioactive substance based on its half-life."""
    return 0.693 / half_life


def decay_rate(initial_quantity: float, decay_const: float) -> float:
    """Returns the decay rate of a radioactive substance based on its initial quantity and decay constant."""
    return decay_const * initial_quantity


def decay_energy(mass_defect: float) -> Quantity:
    """Returns the energy released in a nuclear decay based on the mass defect."""
    return mass_defect * E
