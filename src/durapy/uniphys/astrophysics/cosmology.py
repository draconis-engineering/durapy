"""`UniPhys` cosmology source"""

from ...shared.constants import HUBBLE
from ...shared.numval_types import Quantity
from ...shared.units import METER, NUMERICAL, SECOND

_MPS = METER / SECOND


def redshift(*, λobs: float, λrest: float) -> Quantity:
    """The redshift of a photon based on the wavelength at rest and the observed wavelength"""

    if λrest == 0:
        raise ValueError("Rest wavelength cannot be zero")
    return Quantity((λobs - λrest) / λrest, NUMERICAL)


def hubbles_law(distance: float) -> Quantity:
    if distance <= 0:
        raise ValueError("Distance must be greater than zero")
    return Quantity(HUBBLE.value * distance, _MPS)


__all__ = ["hubbles_law", "redshift"]
