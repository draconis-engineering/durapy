"""UniMath Geometry Module"""

import math


def sas_area(a: float, b: float, C: float) -> float:
    """Returns the area of a triangle from two sides and the included angle."""
    if not all([a, b, C]):
        raise ValueError("sas_area needs three arguments!")
    return 0.5 * a * b * math.sin(math.radians(C))


def herons_formula(a: float, b: float, c: float) -> float:
    """Returns the area of a triangle from the side lengths."""
    if not all([a, b, c]):
        raise ValueError("herons_formula needs three arguments!")
    S = (a + b + c) / 2
    return math.sqrt(S * (S - a) * (S - b) * (S - c))


def polygon_area(n: int, side_length: float) -> float:
    """Returns the area of a regular polygon with `n` sides and a side length of `side_length`."""
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
