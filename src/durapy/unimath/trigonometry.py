"""`UniMath` Trigonometry module"""

import math

import sympy

from .geometry import herons_formula


def interpolate_triangle(
    a: float,
    b: float,
    c: float,
    A: float | None = None,
    B: float | None = None,
    C: float | None = None,
) -> tuple[
    float,
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]:
    """
    Extrapolate the sides of a triangle from the AAAS case (3x Angle + 1x Side)

    Returns
    -------
        Area, (A, B, C), (a, b, c), (sin(a), sin(b), sin(c))
    """

    if sum([a, b, c]) != 180:
        raise ValueError("The sum of the angles of a triangle must be 180 degrees!")

    sin_A = math.sin(math.radians(a))
    sin_B = math.sin(math.radians(b))
    sin_C = math.sin(math.radians(c))

    if A and not B and not C:
        B = (A * sin_B) / sin_A
        C = (A * sin_C) / sin_A

    elif B and not A and not C:
        A = (B * sin_A) / sin_B
        C = (B * sin_C) / sin_B

    elif C and not A and not B:
        A = (C * sin_A) / sin_C
        B = (C * sin_B) / sin_C

    else:
        raise ValueError("A, B, and C cannot all be None!")

    area = herons_formula(A, B, C)

    return area, (A, B, C), (a, b, c), (sin_A, sin_B, sin_C)


def cosine_rule(len_A: float, len_B: float, angle_A: float) -> float:
    return math.sqrt(
        len_A**2 + len_B**2 - ((2 * len_A * len_B) * math.cos(math.radians(angle_A)))
    )


def reverse_cosine_rule(
    len_A: float, len_B: float, len_C: float
) -> tuple[float, float, float]:
    """
    Returns a tuple of the three angles in degrees, in the order of AngleA, AngleB, and AngleC.

    Formula:
        Angle A = arccos( ( B² + C² - A² ) / ( 2 * B * C ) )
    """

    return (
        math.degrees(
            math.acos((len_B**2 + len_C**2 - len_A**2) / (2 * len_B * len_C))
        ),  # AngleA
        math.degrees(
            math.acos((len_C**2 + len_A**2 - len_B**2) / (2 * len_C * len_A))
        ),  # AngleB
        math.degrees(
            math.acos((len_A**2 + len_B**2 - len_C**2) / (2 * len_A * len_B))
        ),  # AngleC
    )


def tangent_formula(func1: str, func2: str) -> list[str]:
    """Returns the tangent(s) between two functions by finding the points where the derivatives are equal and then calculating the slope of the tangent line at those points."""

    x = sympy.symbols("x")
    f1 = sympy.sympify(func1)
    f2 = sympy.sympify(func2)
    df1 = sympy.diff(f1, x)
    df2 = sympy.diff(f2, x)

    slope_eq = sympy.Eq(df1, df2)
    tan_points = sympy.solve(slope_eq, x)
    tangents = []

    for idx, point in enumerate(tan_points, 1):
        string = f"Tangent {idx} - point: {point} - y: {f1.subs(x, point)} - slope: {df1.subs(x, point)}"
        tangents.append(string)

    return tangents
