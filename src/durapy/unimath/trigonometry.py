"""`UniMath` Trigonometry module"""

import math

import sympy

from ._parsing import parse_expression
from .geometry import herons_formula

__all__ = [
    "acos_deg",
    "asin_deg",
    "atan2_deg",
    "atan_deg",
    "cos_deg",
    "cosine_rule",
    "degrees_to_radians",
    "interpolate_triangle",
    "radians_to_degrees",
    "reverse_cosine_rule",
    "sin_deg",
    "tan_deg",
    "tangent_formula",
]


def degrees_to_radians(degrees: float, /) -> float:
    """Convert an angle from degrees to radians."""
    return math.radians(degrees)


def radians_to_degrees(radians: float, /) -> float:
    """Convert an angle from radians to degrees."""
    return math.degrees(radians)


def sin_deg(degrees: float, /) -> float:
    """Return the sine of an angle given in degrees."""
    return math.sin(math.radians(degrees))


def cos_deg(degrees: float, /) -> float:
    """Return the cosine of an angle given in degrees."""
    return math.cos(math.radians(degrees))


def tan_deg(degrees: float, /) -> float:
    """Return the tangent of an angle given in degrees."""
    return math.tan(math.radians(degrees))


def asin_deg(value: float, /) -> float:
    """Return the arcsine of `value` in degrees."""
    return math.degrees(math.asin(value))


def acos_deg(value: float, /) -> float:
    """Return the arccosine of `value` in degrees."""
    return math.degrees(math.acos(value))


def atan_deg(value: float, /) -> float:
    """Return the arctangent of `value` in degrees."""
    return math.degrees(math.atan(value))


def atan2_deg(y: float, x: float) -> float:
    """Return the two-argument arctangent of `y` and `x` in degrees."""
    return math.degrees(math.atan2(y, x))


def _validate_angle(angle: float, name: str) -> None:
    if not 0 < angle < 180:
        raise ValueError(f"{name} must be between 0 and 180 degrees, exclusive")


def _validate_side(side: float, name: str) -> None:
    if side <= 0:
        raise ValueError(f"{name} must be positive")


def interpolate_triangle(
    degA: float,
    degB: float,
    degC: float,
    lenA: float | None = None,
    lenB: float | None = None,
    lenC: float | None = None,
) -> tuple[
    float,
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]:
    """
    Extrapolate the sides of a triangle from three angles and one side.

    The angles are given in degrees. Exactly one side length must be provided.

    Returns
    -------
        Area, (A, B, C), (a, b, c), (sin(a), sin(b), sin(c))
    """

    for name, angle in (("degA", degA), ("degB", degB), ("degC", degC)):
        _validate_angle(angle, name)

    if not math.isclose(degA + degB + degC, 180.0, abs_tol=1e-9):
        raise ValueError("The sum of the angles of a triangle must be 180 degrees!")

    provided = {
        name: value
        for name, value in (("lenA", lenA), ("lenB", lenB), ("lenC", lenC))
        if value is not None
    }
    if len(provided) != 1:
        raise ValueError(
            f"Exactly one side length must be provided, got {len(provided)}"
        )

    side_name, side_value = next(iter(provided.items()))
    _validate_side(side_value, side_name)

    sin_A = sin_deg(degA)
    sin_B = sin_deg(degB)
    sin_C = sin_deg(degC)

    if side_name == "lenA":
        lenA = side_value
        lenB = (lenA * sin_B) / sin_A
        lenC = (lenA * sin_C) / sin_A
    elif side_name == "lenB":
        lenB = side_value
        lenA = (lenB * sin_A) / sin_B
        lenC = (lenB * sin_C) / sin_B
    else:
        lenC = side_value
        lenA = (lenC * sin_A) / sin_C
        lenB = (lenC * sin_B) / sin_C

    area = herons_formula(lenA, lenB, lenC)

    return area, (lenA, lenB, lenC), (degA, degB, degC), (sin_A, sin_B, sin_C)


def cosine_rule(len_A: float, len_B: float, deg_A: float) -> float:
    """
    Return the side opposite `deg_A` given the adjacent sides `len_A` and `len_B`.

    The angle is given in degrees.
    """
    _validate_side(len_A, "len_A")
    _validate_side(len_B, "len_B")
    _validate_angle(deg_A, "deg_A")

    radicand = len_A**2 + len_B**2 - ((2 * len_A * len_B) * cos_deg(deg_A))
    return math.sqrt(max(0.0, radicand))


def _clamp_cos(v: float) -> float:
    return max(-1.0, min(1.0, v))


def reverse_cosine_rule(
    len_A: float, len_B: float, len_C: float
) -> tuple[float, float, float]:
    """
    Returns a tuple of the three angles in degrees, in the order of AngleA, AngleB, and AngleC.

    Formula:
        Angle A = arccos( ( B² + C² - A² ) / ( 2 * B * C ) )

    Raises
    ------
    ValueError
        If any side is not positive or the side lengths violate the triangle inequality.
    """
    for name, side in (("len_A", len_A), ("len_B", len_B), ("len_C", len_C)):
        _validate_side(side, name)

    if len_A + len_B <= len_C or len_A + len_C <= len_B or len_B + len_C <= len_A:
        raise ValueError("Side lengths violate triangle inequality")

    return (
        acos_deg(_clamp_cos((len_B**2 + len_C**2 - len_A**2) / (2 * len_B * len_C))),
        acos_deg(_clamp_cos((len_C**2 + len_A**2 - len_B**2) / (2 * len_C * len_A))),
        acos_deg(_clamp_cos((len_A**2 + len_B**2 - len_C**2) / (2 * len_A * len_B))),
    )


def tangent_formula(f_1: str, f_2: str) -> list[str]:
    """
    Return the points where two functions have equal derivatives.

    This finds parallel tangent points, not necessarily common tangents. Each
    entry describes the point, the function value, and the shared slope.
    """
    if not isinstance(f_1, str) or not isinstance(f_2, str):
        raise TypeError("f_1 and f_2 must be strings")

    x: sympy.Symbol = sympy.symbols("x")
    f1 = parse_expression(f_1)
    f2 = parse_expression(f_2)
    df1 = sympy.diff(f1, x)
    df2 = sympy.diff(f2, x)

    slope_eq = sympy.Eq(df1, df2)
    tan_points = sympy.solve(slope_eq, x)
    tangents: list[str] = []

    for idx, point in enumerate(tan_points, 1):
        string = f"Tangent {idx} - point: {point} - y: {f1.subs(x, point)} - slope: {df1.subs(x, point)}"
        tangents.append(string)

    return tangents
