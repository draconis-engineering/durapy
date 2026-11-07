"""`UniPhys` relativity source"""

from ...shared.constants import C
from ...shared.numval_types import Quantity
from ...shared.units import JOULE


def einstein_mass_energy_equivalence(mass: float) -> Quantity:
    """Returns the rest energy equivalent of a mass via E = mc²."""
    return Quantity(mass * C.value**2, JOULE)


__all__ = ["einstein_mass_energy_equivalence"]
