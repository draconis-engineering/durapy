"""`UniMath` Geometry source"""

import math


def sas_area(a: float, b: float, C: float) -> float:
    """Returns the area of a triangle from two sides and the included angle."""
    if a <= 0 or b <= 0:
        raise ValueError("sas_area requires positive side lengths")
    if not (0 < C < 180):
        raise ValueError("sas_area requires 0 < angle < 180 degrees")
    return 0.5 * a * b * math.sin(math.radians(C))


def herons_formula(a: float, b: float, c: float) -> float:
    """Returns the area of a triangle from the side lengths."""
    if a <= 0 or b <= 0 or c <= 0:
        raise ValueError("herons_formula requires positive side lengths")
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("Side lengths violate triangle inequality")
    S = (a + b + c) / 2
    area_sq = S * (S - a) * (S - b) * (S - c)
    if area_sq < 0:
        # Clamp tiny negative due to floating error
        area_sq = 0.0
    return math.sqrt(area_sq)


def polygon_area(n: int, side_length: float) -> float:
    """Returns the area of a regular polygon with `n` sides and a side length of `side_length`."""
    if n < 3:
        raise ValueError("Polygon must have at least 3 sides")
    if side_length <= 0:
        raise ValueError("Side length must be positive")
    return (n * side_length**2) / (4 * math.tan(math.pi / n))


def polygon_circumference(n: int, side_length: float) -> float:
    """Returns the circumference of a regular polygon with `n` sides and a side length of `side_length`."""
    return n * side_length


def polygon_interior_angle(n: int) -> float:
    """Returns the interior angle of a regular polygon with `n` sides."""
    return (n - 2) * 180 / n


def polygon_exterior_angle(n: int) -> float:
    """Returns the exterior angle of a regular polygon with `n` sides."""
    return 360 / n
