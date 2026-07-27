"""UniMath algebra module."""

import math

import sympy


def slope(x1: float, y1: float, x2: float, y2: float) -> float:
    """Returns the slope of a line from two points `(x1, y1)` and `(x2, y2)`"""
    return (y2 - y1) / (x2 - x1)


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Return the distance between two points `(x1, y1)` and `(x2, y2)`"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def derivative(func: str, x: float | None = None, h: float = 1e-5) -> float:
    """Returns `f'(x)` if `x` is not given, else returns the numerical derivative of the function at the given x-value using the definition of the derivative."""
    x_sym = sympy.symbols("x")
    f = sympy.sympify(func)

    if x is None:
        return float(sympy.diff(f, x_sym))

    else:
        return (f.subs(x_sym, x + h) - f.subs(x_sym, x - h)) / (2 * h)  # type: ignore - 'Basic' arithmetic is apparently invalid


def line_intersection(
    m1: float, b1: float, m2: float, b2: float
) -> tuple[float, float]:
    """ "Return the point of intersection of two lines in the form of `(x, y)`"""
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return (x, y)


def line_from_points(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
    """Returns `m`, `b` as parts of the equation `y = mx + b` from the two given points `(x1, y1)` and `(x2, y2)`."""
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return (m, b)


def linear_zero(m: float, b: float) -> float:
    """Find the x-value where the line `y = mx + b` crosses the x-axis"""
    return -b / m


def linear_evaluation(m: float, b: float, x: float) -> float:
    """Evaluates the linear function `y = mx + b` at `x` and returns the result."""
    return m * x + b


def quadratic_vertex(a: float, b: float, c: float) -> tuple[float, float, str]:
    """Returns the vertex (aka the minimum/maximum point) of a quadratic function in the form of `(x, y)`."""
    xv = -b / (2 * a)
    yv = quadratic_evaluation(a, b, c, xv)

    return xv, yv, "Minimum" if a > 0 else "Maximum" if a < 0 else "Linear"


def quadratic_num_roots(a: float, b: float, c: float) -> int:
    """Returns the number of roots of a quadratic function based on the discriminant."""
    D = b**2 - 4 * a * c
    return 2 if D > 0 else 1 if D == 0 else 0


def quadratic_solutions(
    A: float, B: float, C: float
) -> tuple[float, float] | float | None:
    """Solves quadratic equations and returns x-values in a tuple."""

    if A == 0:
        raise ValueError("Invalid quadratic equation! A cannot be 0.")

    D = B**2 - 4 * A * C

    if D > 0:
        x1 = (-B - math.hypot(0, D)) / (2 * A)
        x2 = (-B + math.hypot(0, D)) / (2 * A)
        return (x1, x2)

    elif D == 0:
        x1 = -B / (2 * A)
        return x1

    else:
        return None


def quadratic_factorized(a: float, b: float, c: float) -> str:
    """Returns the factorized form of a quadratic function in the form of `a(x - x1)(x - x2)` where `x1` and `x2` are the roots of the function."""

    D = b**2 - 4 * a * c

    def sign(x: float) -> str:
        return "-" if x < 0 else "+"

    if D > 0:
        x1 = (-b - math.hypot(0, D)) / (2 * a)
        x2 = (-b + math.hypot(0, D)) / (2 * a)
        return f"{a}(x {sign(x1)} {x1})(x {sign(x2)} {x2})"

    elif D == 0:
        x1 = -b / (2 * a)
        return f"{a}(x {sign(x1)} {x1})²"

    else:
        return f"{a}x² {sign(b)} {abs(b)}x {sign(c)} {abs(c)}"


def quadratic_evaluation(a: float, b: float, c: float, x: float) -> float:
    """Evaluate a quadratic polynomial."""
    return a * x**2 + b * x + c


def cubic_vertex(
    a: float, b: float, c: float, d: float
) -> list[tuple[float, sympy.Basic]]:
    """Returns the vertices (aka the minimum/maximum points) of a cubic function in the form of `(x, y)`."""
    x = sympy.symbols("x")
    f = sympy.sympify(f"{a}*x**3 + {b}*x**2 + {c}*x + {d}")
    dif = sympy.diff(f, x)
    crit_points = sympy.solve(dif, x)
    vertices: list[tuple[float, sympy.Basic]] = []

    for point in crit_points:
        y = f.subs(x, point)
        vertices.append((point, y))

    return vertices


def cubic_num_roots(a: float, b: float, c: float, d: float) -> int:
    """Returns the number of roots of a cubic function based on the discriminant."""
    D = (
        18 * a * b * c * d
        - 4 * b**3 * d
        + b**2 * c**2
        - 4 * a * c**3
        - 27 * a**2 * d**2
    )
    return 3 if D > 0 else 2 if D == 0 else 1


def cubic_solutions(a: float, b: float, c: float, d: float) -> list:
    """Returns the roots of a cubic function in a tuple."""
    x = sympy.symbols("x")
    f = sympy.sympify(f"{a}*x**3 + {b}*x**2 + {c}*x + {d}")
    return sympy.solve(f, x)


def cubic_zeros(a: float, b: float, c: float, d: float) -> list:
    """Returns the x-values where the cubic function crosses the x-axis."""
    x = sympy.symbols("x")
    f = sympy.sympify(f"{a}*x**3 + {b}*x**2 + {c}*x + {d}")
    return sympy.solve(f, x)


def cubic_evaluation(a: float, b: float, c: float, d: float, x: float) -> float:
    """Evaluate a cubic polynomial."""
    return a * x**3 + b * x**2 + c * x + d


def cubic_evaluation_bruteforce(
    a: float, b: float, c: float, d: float, lower: int, upper: int
) -> list[int]:
    """Brute Force evaluation of a third-degree polynomial. The function checks all evaluations from `LowerBound` to `UpperBound` and highlights roots as green."""
    x_vals: list[int] = []
    y_vals: list[float] = []
    roots: list[int] = []

    for x in range(int(lower), int(upper + 1)):
        result = cubic_evaluation(a, b, c, d, x)
        x_vals.append(x)
        y_vals.append(result)
        roots.append(x) if result == 0 else None

    return roots
