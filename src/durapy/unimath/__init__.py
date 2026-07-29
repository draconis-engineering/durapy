"""The UniMath module for DuraPy."""

try:
    # Setuptools places the binary inside the exact module path defined in setup.py
    from . import _maxcompute
except ImportError:
    _maxcompute = None

from . import (
    algebra,
    decorators,
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
    "decorators",
    "geometry",
    "linalg",
    "num_theory",
    "trigonometry",
]
