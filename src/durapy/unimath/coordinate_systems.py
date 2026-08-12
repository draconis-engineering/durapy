"""`UniMath` Coordinate Systems source"""

from __future__ import annotations

import math


class _BaseCoordinate:
    def __init__(self, unit: str, dims: int):
        self.unit = unit
        self.dims = dims


class Cartesian1D(_BaseCoordinate):
    """The 1-dimensional Cartesian coordinate system. (aka. the number line)"""

    def __init__(self, unit: str, x: float):
        super().__init__(unit=unit, dims=1)
        self.x = x


class Cartesian2D(_BaseCoordinate):
    """The 2-dimensional Cartesian coordinate system."""

    def __init__(self, unit: str, x: float, y: float) -> None:
        super().__init__(unit=unit, dims=2)
        self.x = x
        self.y = y

    def to_polar(self) -> Polar:
        return Polar(
            unit=self.unit, r=math.hypot(self.x, self.y), θ=math.atan(self.y / self.x)
        )

    def distance_to_origo(self) -> float:
        return math.hypot(self.x, self.y)


class Cartesian3D(_BaseCoordinate):
    """The 3-dimensional Cartesian coordinate system."""

    def __init__(self, unit: str, x: float, y: float, z: float) -> None:
        super().__init__(unit=unit, dims=3)
        self.x = x
        self.y = y
        self.z = z

    def to_spherical(self) -> Spherical:
        p = math.hypot(self.x, self.y, self.z)

        return Spherical(
            unit=self.unit, r=p, θ=math.atan(self.y / self.x), φ=math.acos(self.z / p)
        )

    def to_cylindrical(self) -> Cylindrical:
        return Cylindrical(
            unit=self.unit,
            r=math.hypot(self.x, self.y, self.z),
            θ=math.atan(self.y / self.x),
            z=self.z,
        )

    def distance_to_origo(self) -> float:
        return math.hypot(self.x, self.y, self.z)


class Polar(_BaseCoordinate):
    """The polar coordinate system."""

    def __init__(self, unit: str, r: float, θ: float) -> None:
        super().__init__(unit=unit, dims=3)
        self.r = r
        self.θ = θ

    def to_cartesian2D(self) -> Cartesian2D:
        return Cartesian2D(
            unit=self.unit, x=self.r * math.cos(self.θ), y=self.r * math.sin(self.θ)
        )

    def distanse_to_origo(self) -> float:
        return self.r


class Spherical(_BaseCoordinate):
    """The spherical coordinate system."""

    def __init__(self, unit: str, r: float, θ: float, φ: float) -> None:
        super().__init__(unit=unit, dims=3)
        self.r = r
        self.θ = θ
        self.φ = φ

    def to_cartesian3D(self) -> Cartesian3D:
        return Cartesian3D(
            unit=self.unit,
            x=self.r * self.φ * math.cos(self.θ),
            y=self.r * self.φ * math.sin(self.θ),
            z=self.r * math.cos(self.φ),
        )

    def to_cylindrical(self) -> Cylindrical:
        return Cylindrical(
            unit=self.unit, r=self.r, θ=self.θ, z=self.r * math.cos(self.φ)
        )

    def distance_to_origo(self) -> float:
        return self.r


class Cylindrical(_BaseCoordinate):
    """The cylindrical coordinate system."""

    def __init__(self, unit: str, r: float, θ: float, z: float) -> None:
        super().__init__(unit=unit, dims=3)
        self.r = r
        self.θ = θ
        self.z = z

    def to_cartesian3D(self) -> Cartesian3D:
        return Cartesian3D(
            unit=self.unit,
            x=self.r * math.sin(self.θ),
            y=self.r * math.cos(self.θ),
            z=self.z,
        )

    def to_spherical(self) -> Spherical:
        dist = math.hypot(self.r, self.z)

        return Spherical(unit=self.unit, r=dist, θ=self.θ, φ=math.acos(self.z / dist))

    def distance_to_origo(self) -> float:
        return math.hypot(self.r, self.z)
