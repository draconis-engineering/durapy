"""`UniMath` Algebra source"""

import math

import dracolix as dlx
import sympy

from ._parsing import parse_expression
from .coordinate_systems import Cartesian2D, Cartesian3D


def _is_close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)


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


__all__ = [
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
    "line_from_cartesian_points",
    "line_from_points",
    "line_intersection",
    "linear_evaluation",
    "linear_zero",
    "point_from_vector",
    "quadratic_evaluation",
    "quadratic_factorized",
    "quadratic_num_roots",
    "quadratic_solutions",
    "quadratic_vertex",
    "slope",
    "slope_from_points",
    "vector_from_point",
]
