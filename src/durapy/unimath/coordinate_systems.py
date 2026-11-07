"""`UniMath` Coordinate Systems source

All angular values in this module are expressed in radians. Use
`unimath.trigonometry.radians_to_degrees` and
`unimath.trigonometry.degrees_to_radians` when converting to or from degrees.
"""

from __future__ import annotations

import math

__all__ = [
    "Cartesian1D",
    "Cartesian2D",
    "Cartesian3D",
    "Cylindrical",
    "Polar",
    "Spherical",
]


def _clamp_unit(value: float) -> float:
    return max(-1.0, min(1.0, value))


class _BaseCoordinate:
    def __init__(self, dims: int, *, unit: str):
        self.dims = dims
        self.unit = unit

    def as_tuple(self) -> tuple[float, ...]:
        """Return the coordinate values in their native order."""
        raise NotImplementedError

    def _to_cartesian_tuple(self) -> tuple[float, ...]:
        raise NotImplementedError

    def distance_to(self, other: _BaseCoordinate) -> float:
        """Return the Euclidean distance to another coordinate of the same dimension and unit."""
        if not isinstance(other, _BaseCoordinate):
            raise TypeError("other must be a coordinate")
        if self.dims != other.dims:
            raise ValueError("Coordinates must have the same number of dimensions")
        if self.unit != other.unit:
            raise ValueError("Coordinates must have the same unit")
        return math.dist(self._to_cartesian_tuple(), other._to_cartesian_tuple())

    def __repr__(self) -> str:
        values = ", ".join(repr(value) for value in self.as_tuple())
        return f"{type(self).__name__}({values}, unit={self.unit!r})"

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        assert isinstance(other, _BaseCoordinate)
        if self.unit != other.unit:
            return False
        return all(
            math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)
            for a, b in zip(self.as_tuple(), other.as_tuple())
        )


class Cartesian1D(_BaseCoordinate):
    """The 1-dimensional Cartesian coordinate system. (aka. the number line)"""

    def __init__(self, x: float, unit: str = "unitless"):
        super().__init__(unit=unit, dims=1)
        self.x = x

    def as_tuple(self) -> tuple[float, ...]:
        return (self.x,)

    def _to_cartesian_tuple(self) -> tuple[float, ...]:
        return self.as_tuple()

    def distance_to_origin(self) -> float:
        return abs(self.x)


class Cartesian2D(_BaseCoordinate):
    """The 2-dimensional Cartesian coordinate system."""

    def __init__(self, x: float, y: float, *, unit: str = "unitless") -> None:
        super().__init__(dims=2, unit=unit)
        self.x = x
        self.y = y

    def as_tuple(self) -> tuple[float, ...]:
        return (self.x, self.y)

    def _to_cartesian_tuple(self) -> tuple[float, ...]:
        return self.as_tuple()

    @classmethod
    def from_polar(cls, r: float, θ: float, *, unit: str = "unitless") -> Cartesian2D:
        """Create a Cartesian point from polar coordinates. `θ` is in radians."""
        return Polar(r, θ, unit=unit).to_cartesian2D()

    def to_polar(self) -> Polar:
        """Convert to polar coordinates. The returned angle is in radians."""
        return Polar(
            unit=self.unit, r=math.hypot(self.x, self.y), θ=math.atan2(self.y, self.x)
        )

    def distance_to_origin(self) -> float:
        return math.hypot(self.x, self.y)


class Cartesian3D(_BaseCoordinate):
    """The 3-dimensional Cartesian coordinate system."""

    def __init__(self, x: float, y: float, z: float, *, unit: str = "unitless") -> None:
        super().__init__(unit=unit, dims=3)
        self.x = x
        self.y = y
        self.z = z

    def as_tuple(self) -> tuple[float, ...]:
        return (self.x, self.y, self.z)

    def _to_cartesian_tuple(self) -> tuple[float, ...]:
        return self.as_tuple()

    @classmethod
    def from_spherical(
        cls, r: float, θ: float, φ: float, *, unit: str = "unitless"
    ) -> Cartesian3D:
        """Create a Cartesian point from spherical coordinates. Angles are in radians."""
        return Spherical(r, θ, φ, unit=unit).to_cartesian3D()

    @classmethod
    def from_cylindrical(
        cls, r: float, θ: float, z: float, *, unit: str = "unitless"
    ) -> Cartesian3D:
        """Create a Cartesian point from cylindrical coordinates. `θ` is in radians."""
        return Cylindrical(r, θ, z, unit=unit).to_cartesian3D()

    def to_spherical(self) -> Spherical:
        """Convert to spherical coordinates. The returned angles are in radians."""
        p = math.hypot(self.x, self.y, self.z)
        if p == 0:
            return Spherical(unit=self.unit, r=0, θ=0, φ=0)
        return Spherical(
            unit=self.unit,
            r=p,
            θ=math.atan2(self.y, self.x),
            φ=math.acos(_clamp_unit(self.z / p)),
        )

    def to_cylindrical(self) -> Cylindrical:
        """Convert to cylindrical coordinates. The returned angle is in radians."""
        return Cylindrical(
            unit=self.unit,
            r=math.hypot(self.x, self.y),
            θ=math.atan2(self.y, self.x),
            z=self.z,
        )

    def distance_to_origin(self) -> float:
        return math.hypot(self.x, self.y, self.z)


class Polar(_BaseCoordinate):
    """The polar coordinate system.

    `r` is the radial distance and `θ` is the azimuth angle in radians,
    measured counter-clockwise from the positive x-axis.
    """

    def __init__(self, r: float, θ: float, *, unit: str = "unitless") -> None:
        super().__init__(unit=unit, dims=2)
        self.r = r
        self.θ = θ

    @property
    def theta(self) -> float:
        """Azimuth angle in radians."""
        return self.θ

    @theta.setter
    def theta(self, value: float) -> None:
        self.θ = value

    @property
    def theta_degrees(self) -> float:
        """Azimuth angle in degrees."""
        return math.degrees(self.θ)

    def as_tuple(self) -> tuple[float, ...]:
        return (self.r, self.θ)

    def _to_cartesian_tuple(self) -> tuple[float, ...]:
        return self.to_cartesian2D().as_tuple()

    @classmethod
    def from_cartesian2D(
        cls, x: float, y: float, *, unit: str = "unitless"
    ) -> Polar:
        """Create a polar coordinate from Cartesian values. `θ` is in radians."""
        return Cartesian2D(x, y, unit=unit).to_polar()

    def to_degrees(self) -> tuple[float, ...]:
        """Return `(r, theta)` with the angle converted to degrees."""
        return (self.r, self.theta_degrees)

    def to_radians(self) -> tuple[float, ...]:
        """Return `(r, theta)` with the angle in radians."""
        return self.as_tuple()

    def to_cartesian2D(self) -> Cartesian2D:
        return Cartesian2D(
            unit=self.unit, x=self.r * math.cos(self.θ), y=self.r * math.sin(self.θ)
        )

    def distance_to_origin(self) -> float:
        return abs(self.r)


class Spherical(_BaseCoordinate):
    """The spherical coordinate system.

    `r` is the radial distance, `θ` is the azimuth angle in radians measured
    counter-clockwise from the positive x-axis in the xy-plane, and `φ` is the
    polar angle in radians measured from the positive z-axis.
    """

    def __init__(self, r: float, θ: float, φ: float, *, unit: str = "unitless") -> None:
        super().__init__(unit=unit, dims=3)
        self.r = r
        self.θ = θ
        self.φ = φ

    @property
    def theta(self) -> float:
        """Azimuth angle in radians."""
        return self.θ

    @theta.setter
    def theta(self, value: float) -> None:
        self.θ = value

    @property
    def phi(self) -> float:
        """Polar angle in radians, measured from the positive z-axis."""
        return self.φ

    @phi.setter
    def phi(self, value: float) -> None:
        self.φ = value

    @property
    def theta_degrees(self) -> float:
        """Azimuth angle in degrees."""
        return math.degrees(self.θ)

    @property
    def phi_degrees(self) -> float:
        """Polar angle in degrees, measured from the positive z-axis."""
        return math.degrees(self.φ)

    def as_tuple(self) -> tuple[float, ...]:
        return (self.r, self.θ, self.φ)

    def _to_cartesian_tuple(self) -> tuple[float, ...]:
        return self.to_cartesian3D().as_tuple()

    @classmethod
    def from_cartesian3D(
        cls, x: float, y: float, z: float, *, unit: str = "unitless"
    ) -> Spherical:
        """Create a spherical coordinate from Cartesian values. Angles are in radians."""
        return Cartesian3D(x, y, z, unit=unit).to_spherical()

    def to_degrees(self) -> tuple[float, ...]:
        """Return `(r, theta, phi)` with both angles converted to degrees."""
        return (self.r, self.theta_degrees, self.phi_degrees)

    def to_radians(self) -> tuple[float, ...]:
        """Return `(r, theta, phi)` with both angles in radians."""
        return self.as_tuple()

    def to_cartesian3D(self) -> Cartesian3D:
        return Cartesian3D(
            unit=self.unit,
            x=self.r * math.sin(self.φ) * math.cos(self.θ),
            y=self.r * math.sin(self.φ) * math.sin(self.θ),
            z=self.r * math.cos(self.φ),
        )

    def to_cylindrical(self) -> Cylindrical:
        return Cylindrical(
            unit=self.unit,
            r=self.r * math.sin(self.φ),
            θ=self.θ,
            z=self.r * math.cos(self.φ),
        )

    def distance_to_origin(self) -> float:
        return abs(self.r)


class Cylindrical(_BaseCoordinate):
    """The cylindrical coordinate system.

    `r` is the radial distance in the xy-plane, `θ` is the azimuth angle in
    radians measured counter-clockwise from the positive x-axis, and `z` is the
    height along the z-axis.
    """

    def __init__(self, r: float, θ: float, z: float, *, unit: str = "unitless") -> None:
        super().__init__(unit=unit, dims=3)
        self.r = r
        self.θ = θ
        self.z = z

    @property
    def theta(self) -> float:
        """Azimuth angle in radians."""
        return self.θ

    @theta.setter
    def theta(self, value: float) -> None:
        self.θ = value

    @property
    def theta_degrees(self) -> float:
        """Azimuth angle in degrees."""
        return math.degrees(self.θ)

    def as_tuple(self) -> tuple[float, ...]:
        return (self.r, self.θ, self.z)

    def _to_cartesian_tuple(self) -> tuple[float, ...]:
        return self.to_cartesian3D().as_tuple()

    @classmethod
    def from_cartesian3D(
        cls, x: float, y: float, z: float, *, unit: str = "unitless"
    ) -> Cylindrical:
        """Create a cylindrical coordinate from Cartesian values. `θ` is in radians."""
        return Cartesian3D(x, y, z, unit=unit).to_cylindrical()

    def to_degrees(self) -> tuple[float, ...]:
        """Return `(r, theta, z)` with the angle converted to degrees."""
        return (self.r, self.theta_degrees, self.z)

    def to_radians(self) -> tuple[float, ...]:
        """Return `(r, theta, z)` with the angle in radians."""
        return self.as_tuple()

    def to_cartesian3D(self) -> Cartesian3D:
        return Cartesian3D(
            unit=self.unit,
            x=self.r * math.cos(self.θ),
            y=self.r * math.sin(self.θ),
            z=self.z,
        )

    def to_spherical(self) -> Spherical:
        dist = math.hypot(self.r, self.z)
        if dist == 0:
            return Spherical(unit=self.unit, r=0, θ=0, φ=0)

        return Spherical(
            unit=self.unit,
            r=dist,
            θ=self.θ,
            φ=math.acos(_clamp_unit(self.z / dist)),
        )

    def distance_to_origin(self) -> float:
        return math.hypot(self.r, self.z)
