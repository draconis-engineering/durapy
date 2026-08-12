"""The UniMath module for DuraPy."""

from . import (
    algebra,
    geometry,
    linalg,
    num_theory,
    trigonometry,
)
from .coordinate_systems import (
    Cartesian1D,
    Cartesian2D,
    Cartesian3D,
    Cylindrical,
    Polar,
    Spherical,
)

__all__ = [
    "Cartesian1D",
    "Cartesian2D",
    "Cartesian3D",
    "Cylindrical",
    "Polar",
    "Spherical",
    "algebra",
    "geometry",
    "linalg",
    "num_theory",
    "trigonometry",
]
