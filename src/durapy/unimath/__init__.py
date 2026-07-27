"""The UniMath module for DuraPy."""

try:
    # Setuptools places the binary inside the exact module path defined in setup.py
    from . import _maxcompute
except ImportError:
    _maxcompute = None

# ... keep the rest of your wrapper functions (mat_mat_mul, etc.) unchanged

from . import (
    algebra,
    algorithms,
    decorators,
    exceptions,
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
    "algorithms",
    "decorators",
    "exceptions",
    "geometry",
    "linalg",
    "num_theory",
    "trigonometry",
]
