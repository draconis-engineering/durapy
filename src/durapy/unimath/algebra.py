"""`UniMath` Algebra source"""

import math
from collections.abc import Sequence
from fractions import Fraction

import dracolix as dlx
import numpy as np
import sympy

from ._parsing import parse_expression
from .coordinate_systems import Cartesian2D, Cartesian3D


def _is_close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)


def _normalize_coefficients(coefficients: Sequence[float]) -> list[float]:
    values = [float(coefficient) for coefficient in coefficients]
    if not values:
        raise ValueError("Coefficient sequence cannot be empty")
    while len(values) > 1 and _is_close(values[0], 0):
        values.pop(0)
    return values


def _normalize_fraction_coefficients(
    coefficients: Sequence[float],
) -> list[Fraction]:
    values = [Fraction(str(coefficient)) for coefficient in coefficients]
    if not values:
        raise ValueError("Coefficient sequence cannot be empty")
    while len(values) > 1 and values[0] == 0:
        values.pop(0)
    return values


def _sympy_polynomial(coefficients: Sequence[float]) -> sympy.Poly:
    values = _normalize_fraction_coefficients(coefficients)
    x = sympy.symbols("x")
    degree = len(values) - 1
    expression = sum(
        coefficient * x ** (degree - index)
        for index, coefficient in enumerate(values)
    )
    return sympy.Poly(expression, x)


def _validate_line_coefficients(a: float, b: float) -> None:
    if _is_close(a, 0) and _is_close(b, 0):
        raise ValueError("Line coefficients A and B cannot both be zero")


def vector_from_point(x: Cartesian2D | Cartesian3D, /) -> dlx.Array:
    return (
        dlx.array([x.x, x.y])
        if isinstance(x, Cartesian2D)
        else dlx.array([x.x, x.y, x.z])
    )


def point_from_vector(x: dlx.Array) -> Cartesian2D | Cartesian3D:
    if x.size == 2:
        return Cartesian2D(x[0], x[1])
    elif x.size == 3:
        return Cartesian3D(x[0], x[1], x[2])
    else:
        raise ValueError("Vector doesnt fit into 2/3D points")


def slope(x1: float, y1: float, x2: float, y2: float) -> float:
    """Returns the slope of a line from two points `(x1, y1)` and `(x2, y2)`"""
    if _is_close(x2, x1):
        raise ValueError("Slope is undefined for vertical line (x1 == x2)")
    return (y2 - y1) / (x2 - x1)


def slope_from_points(*, a: Cartesian2D, b: Cartesian2D):
    """Return the slope between two 2D-cartesian points `a` and `b`"""
    return slope(a.x, a.y, b.x, b.y)


def distance2D(x1: float, y1: float, x2: float, y2: float) -> float:
    """Return the distance between two points `(x1, y1)` and `(x2, y2)`"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def distance_from_2Dpoints(*, a: Cartesian2D, b: Cartesian2D):
    """Return the distance between two 2D-cartesian points `a` and `b`"""
    return distance2D(a.x, a.y, b.x, b.y)


def distance3D(
    x1: float,
    y1: float,
    z1: float,
    x2: float,
    y2: float,
    z2: float,
) -> float:
    """Returns the euclidian distance between 2 3D-points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def distance_from_3Dpoints(*, a: Cartesian3D, b: Cartesian3D) -> float:
    return distance3D(a.x, a.y, a.z, b.x, b.y, b.z)


def derivative(func: str, *, x: float | None = None, h: float = 1e-5):
    """Returns `f'(x)` symbolic if `x` is None, else numerical derivative at x."""
    x_sym = sympy.symbols("x")
    f = parse_expression(func)

    if x is None:
        return sympy.diff(f, x_sym)

    else:
        return float((f.subs(x_sym, x + h) - f.subs(x_sym, x - h)) / (2 * h))  # type: ignore


def line_intersection(m1: float, b1: float, m2: float, b2: float) -> Cartesian2D:
    """Return the point of intersection of two lines in the form of `(x, y)`"""
    if _is_close(m1, m2):
        raise ValueError("Lines are parallel (m1 == m2), no unique intersection")
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return Cartesian2D(x, y)


def line_from_points(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
    """Returns `m`, `b` as parts of the equation `y = mx + b` from the two given points `(x1, y1)` and `(x2, y2)`."""
    if _is_close(x2, x1):
        raise ValueError("Cannot form y=mx+b for vertical line (x1 == x2)")
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return (m, b)


def line_from_cartesian_points(*, a: Cartesian2D, b: Cartesian2D):
    """Returns `m`, `b` as parts of the equation `y = mx + b` from the two given points `(x1, y1)` and `(x2, y2)`."""
    return line_from_points(a.x, a.y, b.x, b.y)


def line_general_from_points(
    x1: float, y1: float, x2: float, y2: float
) -> tuple[float, float, float]:
    """Return `A, B, C` for the line `Ax + By + C = 0` through two points."""
    if _is_close(x1, x2) and _is_close(y1, y2):
        raise ValueError("Two distinct points are required")
    return (y1 - y2, x2 - x1, x1 * y2 - x2 * y1)


def line_general_from_cartesian_points(
    *, a: Cartesian2D, b: Cartesian2D
) -> tuple[float, float, float]:
    """Return `A, B, C` for the line through two Cartesian points."""
    return line_general_from_points(a.x, a.y, b.x, b.y)


def line_general_from_slope_intercept(
    m: float, b: float
) -> tuple[float, float, float]:
    """Return `A, B, C` for `y = mx + b` in general form."""
    return (m, -1.0, b)


def line_slope_intercept_from_general(
    a: float, b: float, c: float
) -> tuple[float, float]:
    """Return `m, b` for the non-vertical line `Ax + By + C = 0`."""
    _validate_line_coefficients(a, b)
    if _is_close(b, 0):
        raise ValueError("Vertical line cannot be written as y = mx + b")
    return (-a / b, -c / b)


def line_through_point_with_slope(
    x: float, y: float, m: float
) -> tuple[float, float, float]:
    """Return `A, B, C` for the line with slope `m` through `(x, y)`."""
    return (m, -1.0, y - m * x)


def line_intersection_general(
    a1: float, b1: float, c1: float, a2: float, b2: float, c2: float
) -> Cartesian2D:
    """Return the intersection of two lines in general form."""
    _validate_line_coefficients(a1, b1)
    _validate_line_coefficients(a2, b2)

    determinant = a1 * b2 - a2 * b1
    if _is_close(determinant, 0):
        raise ValueError("Lines are parallel or coincident")

    x = (b1 * c2 - b2 * c1) / determinant
    y = (c1 * a2 - c2 * a1) / determinant
    return Cartesian2D(x, y)


def lines_are_parallel(a1: float, b1: float, a2: float, b2: float) -> bool:
    """Return True when two lines in general form are parallel."""
    _validate_line_coefficients(a1, b1)
    _validate_line_coefficients(a2, b2)
    return _is_close(a1 * b2 - a2 * b1, 0)


def lines_are_perpendicular(
    a1: float, b1: float, a2: float, b2: float
) -> bool:
    """Return True when two lines in general form are perpendicular."""
    _validate_line_coefficients(a1, b1)
    _validate_line_coefficients(a2, b2)
    return _is_close(a1 * a2 + b1 * b2, 0)


def parallel_line_through_point(
    a: float, b: float, x: float, y: float
) -> tuple[float, float, float]:
    """Return the line parallel to `Ax + By + C = 0` through `(x, y)`."""
    _validate_line_coefficients(a, b)
    return (a, b, -(a * x + b * y))


def perpendicular_line_through_point(
    a: float, b: float, x: float, y: float
) -> tuple[float, float, float]:
    """Return the line perpendicular to `Ax + By + C = 0` through `(x, y)`."""
    _validate_line_coefficients(a, b)
    perpendicular_a, perpendicular_b = b, -a
    return (
        perpendicular_a,
        perpendicular_b,
        -(perpendicular_a * x + perpendicular_b * y),
    )


def point_line_distance(
    a: float, b: float, c: float, x: float, y: float
) -> float:
    """Return the perpendicular distance from `(x, y)` to `Ax + By + C = 0`."""
    _validate_line_coefficients(a, b)
    return abs(a * x + b * y + c) / math.hypot(a, b)


def line_point_projection(
    a: float, b: float, c: float, x: float, y: float
) -> Cartesian2D:
    """Return the foot of the perpendicular from `(x, y)` to a line."""
    _validate_line_coefficients(a, b)
    denominator = a * a + b * b
    offset = a * x + b * y + c
    return Cartesian2D(
        x - (a * offset) / denominator,
        y - (b * offset) / denominator,
    )


def line_contains_point(
    a: float, b: float, c: float, x: float, y: float
) -> bool:
    """Return True when `(x, y)` lies on `Ax + By + C = 0`."""
    _validate_line_coefficients(a, b)
    return _is_close(a * x + b * y + c, 0)


def midpoint(x1: float, y1: float, x2: float, y2: float) -> Cartesian2D:
    """Return the midpoint of two points."""
    return Cartesian2D((x1 + x2) / 2, (y1 + y2) / 2)


def midpoint_from_points(*, a: Cartesian2D, b: Cartesian2D) -> Cartesian2D:
    """Return the midpoint of two Cartesian points."""
    return midpoint(a.x, a.y, b.x, b.y)


def perpendicular_bisector(
    x1: float, y1: float, x2: float, y2: float
) -> tuple[float, float, float]:
    """Return `A, B, C` for the perpendicular bisector of two points."""
    if _is_close(x1, x2) and _is_close(y1, y2):
        raise ValueError("Two distinct points are required")
    return (
        2 * (x2 - x1),
        2 * (y2 - y1),
        x1 * x1 + y1 * y1 - x2 * x2 - y2 * y2,
    )


def circle_equation(
    center_x: float, center_y: float, radius: float
) -> tuple[float, float, float]:
    """Return `D, E, F` for the circle `x² + y² + Dx + Ey + F = 0`."""
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return (
        -2 * center_x,
        -2 * center_y,
        center_x * center_x + center_y * center_y - radius * radius,
    )


def circle_from_equation(
    d: float, e: float, f: float
) -> tuple[float, float, float]:
    """Return `center_x, center_y, radius` from `x² + y² + Dx + Ey + F = 0`."""
    center_x = -d / 2
    center_y = -e / 2
    radius_squared = center_x * center_x + center_y * center_y - f
    if radius_squared < 0 and not _is_close(radius_squared, 0):
        raise ValueError("The equation does not describe a real circle")
    return (center_x, center_y, math.sqrt(max(0.0, radius_squared)))


def circle_from_three_points(
    x1: float, y1: float, x2: float, y2: float, x3: float, y3: float
) -> tuple[float, float, float]:
    """Return `center_x, center_y, radius` for the circle through three points."""
    first_bisector = perpendicular_bisector(x1, y1, x2, y2)
    second_bisector = perpendicular_bisector(x1, y1, x3, y3)
    center = line_intersection_general(*first_bisector, *second_bisector)
    radius = math.hypot(center.x - x1, center.y - y1)
    return (center.x, center.y, radius)


def line_circle_intersection(
    a: float,
    b: float,
    c: float,
    center_x: float,
    center_y: float,
    radius: float,
) -> list[Cartesian2D]:
    """Return the intersection points of a line and a circle."""
    _validate_line_coefficients(a, b)
    if radius < 0:
        raise ValueError("Radius cannot be negative")

    distance = point_line_distance(a, b, c, center_x, center_y)
    if distance > radius and not _is_close(distance, radius):
        return []

    projection = line_point_projection(a, b, c, center_x, center_y)
    if _is_close(distance, radius):
        return [projection]

    half_chord = math.sqrt(max(0.0, radius * radius - distance * distance))
    normal = math.hypot(a, b)
    direction_x, direction_y = b / normal, -a / normal
    return [
        Cartesian2D(
            projection.x - half_chord * direction_x,
            projection.y - half_chord * direction_y,
        ),
        Cartesian2D(
            projection.x + half_chord * direction_x,
            projection.y + half_chord * direction_y,
        ),
    ]


def linear_zero(*, m: float, b: float) -> float:
    """Find the x-value where the line `y = mx + b` crosses the x-axis"""
    if _is_close(m, 0):
        raise ValueError("No zero crossing for horizontal line (m == 0)")
    return -b / m


def linear_evaluation(*, m: float, b: float, x: float) -> float:
    """Evaluates the linear function `y = mx + b` at `x` and returns the result."""
    return m * x + b


def quadratic_vertex(a: float, b: float, c: float) -> tuple[float, float, str]:
    """Returns the vertex (aka the minimum/maximum point) of a quadratic function in the form of `(x, y)`."""
    if _is_close(a, 0):
        raise ValueError("Invalid quadratic equation! A cannot be 0.")

    xv = -b / (2 * a)
    yv = quadratic_evaluation(a, b, c, xv)

    return xv, yv, "Minimum" if a > 0 else "Maximum"


def quadratic_num_roots(a: float, b: float, c: float) -> int:
    """Returns the number of real roots of a quadratic function based on the discriminant."""
    if _is_close(a, 0):
        raise ValueError("Invalid quadratic equation! A cannot be 0.")

    D = b**2 - 4 * a * c
    if _is_close(D, 0):
        return 1
    return 2 if D > 0 else 0


def quadratic_solutions(
    a: float, b: float, c: float
) -> tuple[float, float] | float | None:
    """Solves quadratic equations and returns x-values in a tuple."""

    if _is_close(a, 0):
        raise ValueError("Invalid quadratic equation! A cannot be 0.")

    D = b**2 - 4 * a * c

    if _is_close(D, 0):
        return -b / (2 * a)

    if D > 0:
        sqrtD = math.sqrt(D)
        x1 = (-b - sqrtD) / (2 * a)
        x2 = (-b + sqrtD) / (2 * a)
        return (x1, x2)

    return None


def quadratic_factorized(a: float, b: float, c: float) -> str:
    """Returns the factorized form of a quadratic function in the form of `a(x - x1)(x - x2)` where `x1` and `x2` are the roots of the function."""

    if _is_close(a, 0):
        raise ValueError("Invalid quadratic equation! A cannot be 0.")

    D = b**2 - 4 * a * c

    def sign(x: float) -> str:
        return "-" if x < 0 else "+"

    def factor_str(root: float) -> str:
        if root < 0:
            return f"(x + {-root})"
        return f"(x - {root})"

    if _is_close(D, 0):
        x1 = -b / (2 * a)
        return f"{a}{factor_str(x1)}²"

    if D > 0:
        sqrtD = math.sqrt(D)
        x1 = (-b - sqrtD) / (2 * a)
        x2 = (-b + sqrtD) / (2 * a)
        return f"{a}{factor_str(x1)}{factor_str(x2)}"

    return f"{a}x² {sign(b)} {abs(b)}x {sign(c)} {abs(c)}"


def quadratic_evaluation(a: float, b: float, c: float, x: float) -> float:
    """Evaluate a quadratic polynomial."""
    return a * x**2 + b * x + c


def cubic_vertex(
    a: float, b: float, c: float, d: float
) -> list[tuple[float, sympy.Basic]]:
    """Returns the vertices (aka the minimum/maximum points) of a cubic function in the form of `(x, y)`."""
    x = sympy.symbols("x")
    f = a * x**3 + b * x**2 + c * x + d
    dif = sympy.diff(f, x)
    crit_points = sympy.solve(dif, x)
    vertices: list[tuple[float, sympy.Basic]] = []

    for point in crit_points:
        y = f.subs(x, point)
        vertices.append((point, y))

    return vertices


def cubic_num_roots(a: float, b: float, c: float, d: float) -> int:
    """Returns the number of distinct real roots of a cubic function based on the discriminant."""
    if _is_close(a, 0):
        raise ValueError("Invalid cubic equation! A cannot be 0.")

    D = (
        18 * a * b * c * d
        - 4 * b**3 * d
        + b**2 * c**2
        - 4 * a * c**3
        - 27 * a**2 * d**2
    )
    if _is_close(D, 0):
        return 1 if _is_close(b**2 - 3 * a * c, 0) else 2
    return 3 if D > 0 else 1


def cubic_solutions(a: float, b: float, c: float, d: float) -> list[float]:
    """Returns the roots of a cubic function in a tuple."""
    x = sympy.symbols("x")
    f = a * x**3 + b * x**2 + c * x + d
    return sympy.solve(f, x)


def cubic_zeros(a: float, b: float, c: float, d: float) -> list[float]:
    """Returns the x-values where the cubic function crosses the x-axis."""
    x = sympy.symbols("x")
    f = a * x**3 + b * x**2 + c * x + d
    return sympy.solve(f, x)


def cubic_evaluation(a: float, b: float, c: float, d: float, x: float) -> float:
    """Evaluate a cubic polynomial."""
    return a * x**3 + b * x**2 + c * x + d


def cubic_evaluation_bruteforce(
    a: float, b: float, c: float, d: float, lower: int, upper: int, step: float
) -> list[float]:
    """Brute Force evaluation of a third-degree polynomial. The function checks all evaluations from `LowerBound` to `UpperBound` and highlights roots as green."""
    roots: list[float] = []
    x: float = lower

    while x <= upper:
        result = cubic_evaluation(a, b, c, d, x)
        if math.isclose(result, 0, abs_tol=1e-9):
            roots.append(x)
        x += step

    return roots


def polynomial_degree(coefficients: Sequence[float]) -> int:
    """Return the degree of a polynomial, or -1 for the zero polynomial."""
    values = _normalize_coefficients(coefficients)
    if len(values) == 1 and _is_close(values[0], 0):
        return -1
    return len(values) - 1


def polynomial_leading_coefficient(coefficients: Sequence[float]) -> float:
    """Return the leading coefficient of a polynomial."""
    return _normalize_coefficients(coefficients)[0]


def polynomial_evaluation(coefficients: Sequence[float], x: float) -> float:
    """Evaluate a polynomial at `x` using Horner's method."""
    values = _normalize_coefficients(coefficients)
    result = 0.0
    for coefficient in values:
        result = result * x + coefficient
    return result


def polynomial_derivative(coefficients: Sequence[float]) -> list[float]:
    """Return the derivative coefficients of a polynomial."""
    values = _normalize_coefficients(coefficients)
    degree = len(values) - 1
    if degree < 1:
        return [0.0]
    return [values[index] * (degree - index) for index in range(degree)]


def polynomial_integral(
    coefficients: Sequence[float], constant: float = 0.0
) -> list[float]:
    """Return the antiderivative coefficients of a polynomial."""
    values = _normalize_coefficients(coefficients)
    degree = len(values) - 1
    result = [
        values[index] / (degree - index + 1)
        for index in range(len(values))
    ]
    result.append(float(constant))
    return _normalize_coefficients(result)


def _align_coefficients(
    first: Sequence[float], second: Sequence[float]
) -> tuple[list[float], list[float]]:
    first_values = _normalize_coefficients(first)
    second_values = _normalize_coefficients(second)
    length = max(len(first_values), len(second_values))
    return (
        [0.0] * (length - len(first_values)) + first_values,
        [0.0] * (length - len(second_values)) + second_values,
    )


def polynomial_add(
    first: Sequence[float], second: Sequence[float]
) -> list[float]:
    """Add two polynomials represented by descending coefficients."""
    first_values, second_values = _align_coefficients(first, second)
    return _normalize_coefficients(
        [a + b for a, b in zip(first_values, second_values)]
    )


def polynomial_subtract(
    first: Sequence[float], second: Sequence[float]
) -> list[float]:
    """Subtract two polynomials represented by descending coefficients."""
    first_values, second_values = _align_coefficients(first, second)
    return _normalize_coefficients(
        [a - b for a, b in zip(first_values, second_values)]
    )


def polynomial_multiply(
    first: Sequence[float], second: Sequence[float]
) -> list[float]:
    """Multiply two polynomials represented by descending coefficients."""
    first_values = _normalize_coefficients(first)
    second_values = _normalize_coefficients(second)
    result = [0.0] * (len(first_values) + len(second_values) - 1)
    for first_index, first_coefficient in enumerate(first_values):
        for second_index, second_coefficient in enumerate(second_values):
            result[first_index + second_index] += (
                first_coefficient * second_coefficient
            )
    return _normalize_coefficients(result)


def polynomial_long_division(
    dividend: Sequence[float], divisor: Sequence[float]
) -> tuple[list[float], list[float]]:
    """Return `(quotient, remainder)` for polynomial long division."""
    dividend_values = _normalize_coefficients(dividend)
    divisor_values = _normalize_coefficients(divisor)

    if len(divisor_values) == 1 and _is_close(divisor_values[0], 0):
        raise ValueError("Cannot divide by the zero polynomial")
    if len(dividend_values) < len(divisor_values):
        return [0.0], dividend_values

    quotient_length = len(dividend_values) - len(divisor_values) + 1
    quotient = [0.0] * quotient_length
    remainder = dividend_values[:]

    for index in range(quotient_length):
        coefficient = remainder[index] / divisor_values[0]
        quotient[index] = coefficient
        for divisor_index, divisor_coefficient in enumerate(divisor_values):
            remainder[index + divisor_index] -= (
                coefficient * divisor_coefficient
            )

    remainder_values = remainder[quotient_length:]
    return (
        _normalize_coefficients(quotient),
        _normalize_coefficients(remainder_values) if remainder_values else [0.0],
    )


def polynomial_synthetic_division(
    coefficients: Sequence[float], root: float
) -> tuple[list[float], float]:
    """Return `(quotient, remainder)` from synthetic division by `x - root`."""
    values = _normalize_coefficients(coefficients)
    if len(values) < 2:
        return [0.0], values[0]

    quotient = [values[0]]
    for coefficient in values[1:]:
        quotient.append(coefficient + quotient[-1] * root)

    remainder = quotient.pop()
    return _normalize_coefficients(quotient), remainder


def polynomial_roots(coefficients: Sequence[float]) -> list[complex]:
    """Return all complex roots of a polynomial."""
    values = _normalize_coefficients(coefficients)
    if len(values) == 1:
        if _is_close(values[0], 0):
            raise ValueError("The zero polynomial has infinitely many roots")
        return []
    return [complex(root) for root in np.roots(values)]


def polynomial_real_roots(
    coefficients: Sequence[float], *, tolerance: float = 1e-9
) -> list[float]:
    """Return the real roots of a polynomial, sorted ascending."""
    roots = polynomial_roots(coefficients)
    real_roots = [root.real for root in roots if abs(root.imag) <= tolerance]
    return sorted(real_roots)


def polynomial_rational_roots(
    coefficients: Sequence[float],
) -> list[Fraction]:
    """Return the distinct rational roots of a polynomial."""
    values = _normalize_fraction_coefficients(coefficients)
    if len(values) == 1:
        if values[0] == 0:
            raise ValueError("The zero polynomial has infinitely many roots")
        return []

    roots = sympy.ground_roots(_sympy_polynomial(values))
    return sorted(
        {Fraction(int(root.p), int(root.q)) for root in roots}
    )


def polynomial_factorized(coefficients: Sequence[float]) -> str:
    """Return the factored form of a polynomial as a string."""
    return str(sympy.factor(_sympy_polynomial(coefficients).as_expr()))


def polynomial_from_roots(
    roots: Sequence[float], *, leading_coefficient: float = 1.0
) -> list[float]:
    """Return descending coefficients for a polynomial with the given roots."""
    if _is_close(leading_coefficient, 0):
        raise ValueError("Leading coefficient cannot be zero")

    coefficients = [float(leading_coefficient)]
    for root in roots:
        expanded = [0.0] * (len(coefficients) + 1)
        for index, coefficient in enumerate(coefficients):
            expanded[index] += coefficient
            expanded[index + 1] -= coefficient * root
        coefficients = expanded
    return _normalize_coefficients(coefficients)


__all__ = [
    "circle_equation",
    "circle_from_equation",
    "circle_from_three_points",
    "cubic_evaluation",
    "cubic_evaluation_bruteforce",
    "cubic_num_roots",
    "cubic_solutions",
    "cubic_vertex",
    "cubic_zeros",
    "derivative",
    "distance2D",
    "distance3D",
    "distance_from_2Dpoints",
    "distance_from_3Dpoints",
    "line_circle_intersection",
    "line_contains_point",
    "line_from_cartesian_points",
    "line_from_points",
    "line_general_from_cartesian_points",
    "line_general_from_points",
    "line_general_from_slope_intercept",
    "line_intersection",
    "line_intersection_general",
    "line_point_projection",
    "line_slope_intercept_from_general",
    "line_through_point_with_slope",
    "linear_evaluation",
    "linear_zero",
    "lines_are_parallel",
    "lines_are_perpendicular",
    "midpoint",
    "midpoint_from_points",
    "parallel_line_through_point",
    "perpendicular_bisector",
    "perpendicular_line_through_point",
    "point_from_vector",
    "point_line_distance",
    "polynomial_add",
    "polynomial_degree",
    "polynomial_derivative",
    "polynomial_evaluation",
    "polynomial_factorized",
    "polynomial_from_roots",
    "polynomial_integral",
    "polynomial_leading_coefficient",
    "polynomial_long_division",
    "polynomial_multiply",
    "polynomial_rational_roots",
    "polynomial_real_roots",
    "polynomial_roots",
    "polynomial_subtract",
    "polynomial_synthetic_division",
    "quadratic_evaluation",
    "quadratic_factorized",
    "quadratic_num_roots",
    "quadratic_solutions",
    "quadratic_vertex",
    "slope",
    "slope_from_points",
    "vector_from_point",
]
