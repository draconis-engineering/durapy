"""Correctness and validation tests for the unimath package."""

import math
from fractions import Fraction

import dracolix as dlx
import pytest

from durapy.unimath import (
    algebra,
    geometry,
    num_theory,
)
from durapy.unimath import (
    coordinate_systems as cs,
)
from durapy.unimath import (
    trigonometry as trig,
)


def test_degree_radian_helpers_roundtrip():
    assert trig.degrees_to_radians(180) == pytest.approx(math.pi)
    assert trig.radians_to_degrees(math.pi) == pytest.approx(180)
    assert trig.radians_to_degrees(trig.degrees_to_radians(37.5)) == pytest.approx(37.5)


def test_degree_trig_helpers():
    assert trig.sin_deg(30) == pytest.approx(0.5)
    assert trig.cos_deg(60) == pytest.approx(0.5)
    assert trig.tan_deg(45) == pytest.approx(1.0)
    assert trig.asin_deg(0.5) == pytest.approx(30)
    assert trig.acos_deg(0.5) == pytest.approx(60)
    assert trig.atan_deg(1) == pytest.approx(45)
    assert trig.atan2_deg(1, 1) == pytest.approx(45)


def test_interpolate_equilateral_triangle():
    area, sides, angles, sines = trig.interpolate_triangle(60, 60, 60, lenA=1)

    assert area == pytest.approx(math.sqrt(3) / 4)
    assert sides == pytest.approx((1, 1, 1))
    assert angles == (60, 60, 60)
    assert sines == pytest.approx((math.sqrt(3) / 2,) * 3)


@pytest.mark.parametrize("side_name", ["lenA", "lenB", "lenC"])
def test_interpolate_triangle_supports_each_side(side_name):
    side = 1 if side_name == "lenA" else math.sqrt(3) if side_name == "lenB" else 2
    area, sides, _, _ = trig.interpolate_triangle(30, 60, 90, **{side_name: side})

    assert sides == pytest.approx((1, math.sqrt(3), 2))
    assert area == pytest.approx(math.sqrt(3) / 2)


@pytest.mark.parametrize(
    "angles, sides",
    [
        ((90, 45, 30), {"lenA": 1}),
        ((180, 0, 0), {"lenA": 1}),
        ((60, 60, 60), {"lenA": -1}),
        ((60, 60, 60), {}),
        ((60, 60, 60), {"lenA": 1, "lenB": 1}),
    ],
)
def test_interpolate_triangle_rejects_invalid_inputs(angles, sides):
    with pytest.raises(ValueError):
        trig.interpolate_triangle(*angles, **sides)


def test_cosine_rule():
    assert trig.cosine_rule(3, 4, 90) == pytest.approx(5)
    assert trig.cosine_rule(1, 1, 60) == pytest.approx(1)


@pytest.mark.parametrize(
    "args",
    [(0, 1, 90), (1, 0, 90), (1, 1, 0), (1, 1, 180), (1, 1, -10)],
)
def test_cosine_rule_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        trig.cosine_rule(*args)


def test_reverse_cosine_rule():
    angles = trig.reverse_cosine_rule(3, 4, 5)

    assert angles == pytest.approx(
        (
            math.degrees(math.acos(0.8)),
            math.degrees(math.acos(0.6)),
            90,
        )
    )
    assert trig.reverse_cosine_rule(1, 1, 1) == pytest.approx((60, 60, 60))


@pytest.mark.parametrize(
    "sides",
    [(1, 1, 10), (1, 2, 3), (0, 1, 1), (-1, 1, 1)],
)
def test_reverse_cosine_rule_rejects_invalid_triangles(sides):
    with pytest.raises(ValueError):
        trig.reverse_cosine_rule(*sides)


def test_tangent_formula_returns_equal_derivative_points():
    tangents = trig.tangent_formula("x**2", "x**3")

    assert len(tangents) == 2
    assert "point: 0" in tangents[0]


def test_tangent_formula_requires_strings():
    with pytest.raises(TypeError):
        trig.tangent_formula(1, "x")


def test_cartesian1d_distance_to_origin():
    assert cs.Cartesian1D(-4).distance_to_origin() == 4


def test_cartesian2d_polar_roundtrip():
    polar = cs.Cartesian2D(1, 1).to_polar()
    assert polar.r == pytest.approx(math.sqrt(2))
    assert polar.θ == pytest.approx(math.pi / 4)

    cartesian = polar.to_cartesian2D()
    assert cartesian.x == pytest.approx(1)
    assert cartesian.y == pytest.approx(1)


def test_cartesian3d_spherical_roundtrip():
    original = cs.Cartesian3D(1, 2, 3)
    spherical = original.to_spherical()
    restored = spherical.to_cartesian3D()

    assert restored.x == pytest.approx(original.x)
    assert restored.y == pytest.approx(original.y)
    assert restored.z == pytest.approx(original.z)


@pytest.mark.parametrize(
    "point, expected_theta, expected_phi",
    [
        (cs.Cartesian3D(0, 0, 1), 0, 0),
        (cs.Cartesian3D(1, 0, 0), 0, math.pi / 2),
        (cs.Cartesian3D(0, 1, 0), math.pi / 2, math.pi / 2),
        (cs.Cartesian3D(0, 0, -1), 0, math.pi),
    ],
)
def test_cartesian3d_spherical_angles(point, expected_theta, expected_phi):
    spherical = point.to_spherical()
    assert spherical.θ == pytest.approx(expected_theta)
    assert spherical.φ == pytest.approx(expected_phi)


def test_cartesian3d_cylindrical_roundtrip():
    original = cs.Cartesian3D(1, 2, 3)
    cylindrical = original.to_cylindrical()
    restored = cylindrical.to_cartesian3D()

    assert restored.x == pytest.approx(original.x)
    assert restored.y == pytest.approx(original.y)
    assert restored.z == pytest.approx(original.z)


def test_spherical_to_cylindrical_uses_projected_radius():
    cylindrical = cs.Spherical(2, 0, math.pi / 4).to_cylindrical()

    assert cylindrical.r == pytest.approx(math.sqrt(2))
    assert cylindrical.z == pytest.approx(math.sqrt(2))


def test_spherical_cartesian_roundtrip():
    original = cs.Spherical(2, math.pi / 3, math.pi / 4)
    restored = original.to_cartesian3D().to_spherical()

    assert restored.r == pytest.approx(original.r)
    assert restored.θ == pytest.approx(original.θ)
    assert restored.φ == pytest.approx(original.φ)


def test_cylindrical_spherical_roundtrip():
    original = cs.Cylindrical(2, math.pi / 3, 4)
    restored = original.to_spherical().to_cylindrical()

    assert restored.r == pytest.approx(original.r)
    assert restored.θ == pytest.approx(original.θ)
    assert restored.z == pytest.approx(original.z)


def test_cylindrical_origin_converts_to_spherical():
    spherical = cs.Cylindrical(0, 0, 0).to_spherical()

    assert spherical.r == 0
    assert spherical.θ == 0
    assert spherical.φ == 0


def test_ascii_angle_aliases():
    polar = cs.Polar(1, 0.5)
    assert polar.theta == polar.θ
    polar.theta = 1.5
    assert polar.θ == 1.5

    spherical = cs.Spherical(1, 0.5, 0.25)
    assert spherical.theta == spherical.θ
    assert spherical.phi == spherical.φ
    spherical.phi = 1.25
    assert spherical.φ == 1.25

    cylindrical = cs.Cylindrical(1, 0.5, 2)
    assert cylindrical.theta == cylindrical.θ
    cylindrical.theta = 1.5
    assert cylindrical.θ == 1.5


def test_distance_to_origin_handles_negative_radii():
    assert cs.Polar(-3, 0).distance_to_origin() == 3
    assert cs.Spherical(-3, 0, 0).distance_to_origin() == 3


def test_coordinate_as_tuple():
    assert cs.Cartesian1D(1).as_tuple() == (1,)
    assert cs.Cartesian2D(1, 2).as_tuple() == (1, 2)
    assert cs.Cartesian3D(1, 2, 3).as_tuple() == (1, 2, 3)
    assert cs.Polar(1, 0.5).as_tuple() == (1, 0.5)
    assert cs.Spherical(1, 0.5, 0.25).as_tuple() == (1, 0.5, 0.25)
    assert cs.Cylindrical(1, 0.5, 2).as_tuple() == (1, 0.5, 2)


def test_coordinate_repr_and_equality():
    assert cs.Cartesian2D(1, 2) == cs.Cartesian2D(1, 2)
    assert cs.Cartesian2D(1, 2) == cs.Cartesian2D(1 + 1e-13, 2)
    assert cs.Cartesian2D(1, 2) != cs.Cartesian2D(1, 3)
    assert cs.Cartesian2D(1, 2) != cs.Cartesian2D(1, 2, unit="m")
    assert cs.Cartesian2D(1, 2) != cs.Polar(1, 2)
    assert repr(cs.Cartesian2D(1, 2)) == "Cartesian2D(1, 2, unit='unitless')"


def test_coordinate_distance_to():
    assert cs.Cartesian1D(0).distance_to(cs.Cartesian1D(3)) == 3
    assert cs.Cartesian2D(0, 0).distance_to(cs.Cartesian2D(3, 4)) == 5
    assert cs.Cartesian2D(0, 0).distance_to(cs.Polar(3, 0)) == 3
    assert cs.Cartesian3D(0, 0, 0).distance_to(cs.Spherical(1, 0, 0)) == 1
    assert cs.Cartesian3D(0, 0, 0).distance_to(
        cs.Cylindrical(1, 0, 1)
    ) == pytest.approx(math.sqrt(2))


def test_coordinate_distance_to_validation():
    with pytest.raises(TypeError):
        cs.Cartesian1D(0).distance_to(1)
    with pytest.raises(ValueError):
        cs.Cartesian1D(0).distance_to(cs.Cartesian2D(0, 0))
    with pytest.raises(ValueError):
        cs.Cartesian1D(0, unit="m").distance_to(cs.Cartesian1D(1))


def test_cartesian_from_polar():
    assert cs.Cartesian2D.from_polar(1, 0) == cs.Cartesian2D(1, 0)

    point = cs.Cartesian2D.from_polar(2, math.pi / 2, unit="m")
    assert point == cs.Cartesian2D(0, 2, unit="m")


def test_cartesian_from_spherical():
    assert cs.Cartesian3D.from_spherical(1, 0, 0) == cs.Cartesian3D(0, 0, 1)
    assert cs.Cartesian3D.from_spherical(2, math.pi / 2, math.pi / 2) == cs.Cartesian3D(
        0, 2, 0
    )


def test_cartesian_from_cylindrical():
    assert cs.Cartesian3D.from_cylindrical(1, 0, 2) == cs.Cartesian3D(1, 0, 2)


def test_coordinate_from_cartesian_constructors():
    polar = cs.Polar.from_cartesian2D(1, 1)
    assert polar.r == pytest.approx(math.sqrt(2))
    assert polar.θ == pytest.approx(math.pi / 4)

    spherical = cs.Spherical.from_cartesian3D(0, 0, 1)
    assert spherical.r == 1
    assert spherical.φ == 0

    cylindrical = cs.Cylindrical.from_cartesian3D(1, 0, 2)
    assert cylindrical.r == 1
    assert cylindrical.θ == 0
    assert cylindrical.z == 2


def test_coordinate_degree_accessors():
    polar = cs.Polar(2, math.pi)
    assert polar.theta_degrees == pytest.approx(180)
    assert polar.to_degrees() == pytest.approx((2, 180))
    assert polar.to_radians() == pytest.approx((2, math.pi))

    spherical = cs.Spherical(1, math.pi / 2, math.pi)
    assert spherical.theta_degrees == pytest.approx(90)
    assert spherical.phi_degrees == pytest.approx(180)
    assert spherical.to_degrees() == pytest.approx((1, 90, 180))
    assert spherical.to_radians() == pytest.approx((1, math.pi / 2, math.pi))

    cylindrical = cs.Cylindrical(1, math.pi / 2, 2)
    assert cylindrical.theta_degrees == pytest.approx(90)
    assert cylindrical.to_degrees() == pytest.approx((1, 90, 2))
    assert cylindrical.to_radians() == pytest.approx((1, math.pi / 2, 2))


def test_sas_area():
    assert geometry.sas_area(2, 3, 90) == pytest.approx(3)


def test_herons_formula():
    assert geometry.herons_formula(3, 4, 5) == pytest.approx(6)


@pytest.mark.parametrize("sides", [(1, 1, 10), (0, 1, 1), (-1, 1, 1)])
def test_herons_formula_rejects_invalid_triangles(sides):
    with pytest.raises(ValueError):
        geometry.herons_formula(*sides)


def test_regular_polygon_helpers():
    assert geometry.polygon_area(4, 2) == pytest.approx(4)
    assert geometry.polygon_circumference(4, 2) == pytest.approx(8)
    assert geometry.polygon_interior_angle(4) == pytest.approx(90)
    assert geometry.polygon_exterior_angle(4) == pytest.approx(90)


@pytest.mark.parametrize("n", [0, 2, -1])
def test_regular_polygon_helpers_reject_too_few_sides(n):
    with pytest.raises(ValueError):
        geometry.polygon_area(n, 1)
    with pytest.raises(ValueError):
        geometry.polygon_circumference(n, 1)
    with pytest.raises(ValueError):
        geometry.polygon_interior_angle(n)
    with pytest.raises(ValueError):
        geometry.polygon_exterior_angle(n)


def test_regular_polygon_helpers_reject_non_integer_sides():
    with pytest.raises(TypeError):
        geometry.polygon_area(4.0, 1)


@pytest.mark.parametrize("side_length", [0, -1])
def test_regular_polygon_helpers_reject_non_positive_side(side_length):
    with pytest.raises(ValueError):
        geometry.polygon_area(4, side_length)
    with pytest.raises(ValueError):
        geometry.polygon_circumference(4, side_length)


def test_fibonacci_integer():
    assert num_theory.fibonacci_integer(0) == 0
    assert num_theory.fibonacci_integer(1) == 1
    assert num_theory.fibonacci_integer(10) == 55


def test_fibonacci_list():
    assert num_theory.fibonacci_list(0) == []
    assert num_theory.fibonacci_list(1) == [0]
    assert num_theory.fibonacci_list(2) == [0, 1]
    assert num_theory.fibonacci_list(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


@pytest.mark.parametrize("value", [1.5, "a", True])
def test_fibonacci_rejects_invalid_values(value):
    with pytest.raises(TypeError):
        num_theory.fibonacci_integer(value)
    with pytest.raises(TypeError):
        num_theory.fibonacci_list(value)


def test_factorial_and_subfactorial():
    assert num_theory.factorial(0) == 1
    assert num_theory.factorial(5) == 120
    assert [num_theory.subfactorial(n) for n in range(6)] == [1, 0, 1, 2, 9, 44]


@pytest.mark.parametrize("func", [num_theory.factorial, num_theory.subfactorial])
@pytest.mark.parametrize("value", [1.5, "a", True, None])
def test_factorial_helpers_reject_invalid_values(func, value):
    with pytest.raises(TypeError):
        func(value)


def test_gcd_and_lcm():
    assert num_theory.gcd(12, 18) == 6
    assert num_theory.lcm(4, 6) == 12


def test_prime_factorize():
    assert num_theory.prime_factorize(360) == [2, 2, 2, 3, 3, 5]
    assert num_theory.prime_factorize(1) == []


@pytest.mark.parametrize("value", [1.5, "a", -0.1])
def test_prime_factorize_rejects_invalid_values(value):
    with pytest.raises(TypeError):
        num_theory.prime_factorize(value)


@pytest.mark.parametrize(
    "value, expected",
    [(2, True), (3, True), (4, False), (1, False), (-7, False)],
)
def test_is_prime(value, expected):
    assert num_theory.is_prime(value) is expected


@pytest.mark.parametrize("value", [1.5, "a", -0.1])
def test_is_prime_rejects_non_integers(value):
    with pytest.raises(TypeError):
        num_theory.is_prime(value)


@pytest.mark.parametrize(
    "value, expected",
    [(0, True), (9, True), (10, False), (-9, False)],
)
def test_is_perfect_square(value, expected):
    assert num_theory.is_perfect_square(value) is expected


@pytest.mark.parametrize(
    "value, expected",
    [(0, True), (8, True), (-8, True), (27, True), (-27, True), (9, False)],
)
def test_is_perfect_cube(value, expected):
    assert num_theory.is_perfect_cube(value) is expected


@pytest.mark.parametrize(
    "value, expected",
    [(8, True), (9, True), (16, True), (64, True), (10, False)],
)
def test_is_perfect_power(value, expected):
    assert num_theory.is_perfect_power(value) is expected


def test_divisor_classification():
    assert num_theory.is_perfect_number(6) is True
    assert num_theory.is_perfect_number(28) is True
    assert num_theory.is_perfect_number(12) is False
    assert num_theory.is_abundant_number(12) is True
    assert num_theory.is_abundant_number(8) is False
    assert num_theory.is_deficient_number(8) is True
    assert num_theory.is_deficient_number(12) is False


def test_amicable_pair():
    assert num_theory.is_amicable_pair(220, 284) is True
    assert num_theory.is_amicable_pair(220, 285) is False


def test_sociable_chain():
    assert num_theory.is_sociable_chain([]) is False
    assert num_theory.is_sociable_chain([6]) is True
    assert num_theory.is_sociable_chain([220, 284]) is True
    assert num_theory.is_sociable_chain([220, 285]) is False
    assert num_theory.is_sociable_chain([0]) is False


def test_sociable_chain_requires_a_list():
    with pytest.raises(TypeError):
        num_theory.is_sociable_chain((6,))


def test_lovelace():
    assert num_theory.lovelace(2, 3, 8, 4, 5, 14) == pytest.approx((1, 2))

    with pytest.raises(ValueError):
        num_theory.lovelace(1, 2, 3, 2, 4, 6)


def test_slope_and_line_helpers():
    assert algebra.slope(0, 0, 1, 1) == 1
    assert algebra.line_from_points(0, 0, 1, 1) == (1, 0)
    assert algebra.linear_zero(m=2, b=-4) == 2

    with pytest.raises(ValueError):
        algebra.slope(1, 0, 1, 1)
    with pytest.raises(ValueError):
        algebra.line_from_points(1, 0, 1, 1)
    with pytest.raises(ValueError):
        algebra.linear_zero(m=0, b=4)


def test_line_intersection():
    point = algebra.line_intersection(1, 0, -1, 2)

    assert point.x == pytest.approx(1)
    assert point.y == pytest.approx(1)

    with pytest.raises(ValueError):
        algebra.line_intersection(1, 0, 1, 2)


def test_quadratic_vertex():
    assert algebra.quadratic_vertex(1, 0, 0) == (0, 0, "Minimum")
    assert algebra.quadratic_vertex(-1, 0, 0) == (0, 0, "Maximum")

    with pytest.raises(ValueError):
        algebra.quadratic_vertex(0, 1, 1)


def test_quadratic_num_roots():
    assert algebra.quadratic_num_roots(1, -3, 2) == 2
    assert algebra.quadratic_num_roots(1, -2, 1) == 1
    assert algebra.quadratic_num_roots(1, 0, 1) == 0

    with pytest.raises(ValueError):
        algebra.quadratic_num_roots(0, 1, 1)


def test_quadratic_solutions():
    assert algebra.quadratic_solutions(1, -3, 2) == pytest.approx((1, 2))
    assert algebra.quadratic_solutions(1, -2, 1) == pytest.approx(1)
    assert algebra.quadratic_solutions(1, 0, 1) is None

    with pytest.raises(ValueError):
        algebra.quadratic_solutions(0, 1, 1)


def test_quadratic_factorized():
    assert algebra.quadratic_factorized(1, -3, 2) == "1(x - 1.0)(x - 2.0)"
    assert algebra.quadratic_factorized(1, -2, 1) == "1(x - 1.0)²"
    assert algebra.quadratic_factorized(1, 0, 1) == "1x² + 0x + 1"

    with pytest.raises(ValueError):
        algebra.quadratic_factorized(0, 1, 1)


def test_cubic_num_roots():
    assert algebra.cubic_num_roots(1, 0, -1, 0) == 3
    assert algebra.cubic_num_roots(1, 0, 0, 0) == 1
    assert algebra.cubic_num_roots(1, 0, 1, 0) == 1
    assert algebra.cubic_num_roots(1, 0, -3, 2) == 2

    with pytest.raises(ValueError):
        algebra.cubic_num_roots(0, 1, 1, 1)


def test_cubic_evaluation_and_bruteforce():
    assert algebra.cubic_evaluation(1, 0, -1, 0, 2) == 6
    assert algebra.cubic_evaluation_bruteforce(1, 0, -1, 0, -2, 2, 1) == [-1, 0, 1]


def test_polynomial_basics():
    assert algebra.polynomial_degree([0, 2, 3]) == 1
    assert algebra.polynomial_degree([0]) == -1
    assert algebra.polynomial_leading_coefficient([0, 2, 3]) == 2
    assert algebra.polynomial_evaluation([2, -3, 1], 2) == 3
    assert algebra.polynomial_derivative([2, -3, 1]) == [4.0, -3.0]
    assert algebra.polynomial_integral([3, 0], 4) == [1.5, 0.0, 4.0]

    with pytest.raises(ValueError):
        algebra.polynomial_degree([])


def test_polynomial_arithmetic():
    assert algebra.polynomial_add([1, 2], [3]) == [1.0, 5.0]
    assert algebra.polynomial_subtract([1, 2], [1, 5]) == [-3.0]
    assert algebra.polynomial_multiply([1, 1], [1, -1]) == [1.0, 0.0, -1.0]
    assert algebra.polynomial_long_division([1, 0, -1], [1, -1]) == (
        [1.0, 1.0],
        [0.0],
    )
    assert algebra.polynomial_long_division([1, 0, 0], [1, -1]) == (
        [1.0, 1.0],
        [1.0],
    )
    assert algebra.polynomial_long_division([2, 4], [2]) == (
        [1.0, 2.0],
        [0.0],
    )
    assert algebra.polynomial_synthetic_division([1, -3, 2], 1) == (
        [1.0, -2.0],
        0.0,
    )

    with pytest.raises(ValueError):
        algebra.polynomial_long_division([1, 2], [0])


def test_polynomial_roots_and_factoring():
    assert sorted(
        algebra.polynomial_roots([1, 0, 1]), key=lambda root: root.imag
    ) == pytest.approx([-1j, 1j])
    assert algebra.polynomial_real_roots([1, 0, -1]) == pytest.approx([-1, 1])
    assert algebra.polynomial_rational_roots([2, -3, 1]) == [
        Fraction(1, 2),
        Fraction(1),
    ]
    assert algebra.polynomial_factorized([1, -3, 2]) == "(x - 2)*(x - 1)"
    assert algebra.polynomial_from_roots([1, 2], leading_coefficient=2) == [
        2.0,
        -6.0,
        4.0,
    ]

    with pytest.raises(ValueError):
        algebra.polynomial_roots([0])
    with pytest.raises(ValueError):
        algebra.polynomial_rational_roots([0])
    with pytest.raises(ValueError):
        algebra.polynomial_from_roots([1], leading_coefficient=0)


def test_polynomial_zero_and_constant_edges():
    assert algebra.polynomial_factorized([0]) == "0"
    assert algebra.polynomial_roots([5]) == []
    assert algebra.polynomial_rational_roots([5]) == []
    assert algebra.polynomial_real_roots([5]) == []
    assert algebra.polynomial_long_division([1, 2], [1, 0, 0]) == (
        [0.0],
        [1.0, 2.0],
    )


def test_general_line_forms():
    line = algebra.line_general_from_points(0, 0, 1, 1)
    assert algebra.line_contains_point(*line, 2, 2)
    assert algebra.line_general_from_cartesian_points(
        a=cs.Cartesian2D(0, 0), b=cs.Cartesian2D(1, 1)
    ) == pytest.approx(line)
    assert algebra.line_general_from_slope_intercept(2, 3) == (2, -1.0, 3)
    assert algebra.line_slope_intercept_from_general(2, -1, 3) == (2, 3)
    assert algebra.line_through_point_with_slope(1, 2, 3) == (3, -1.0, -1)

    vertical = algebra.line_general_from_points(1, 0, 1, 2)
    assert algebra.line_contains_point(*vertical, 1, 42)

    with pytest.raises(ValueError):
        algebra.line_general_from_points(1, 1, 1, 1)
    with pytest.raises(ValueError):
        algebra.line_slope_intercept_from_general(0, 0, 1)
    with pytest.raises(ValueError):
        algebra.line_slope_intercept_from_general(*vertical)


def test_general_line_relationships():
    assert algebra.line_intersection_general(1, 0, -1, 0, 1, -1) == (
        cs.Cartesian2D(1, 1)
    )
    assert algebra.lines_are_parallel(1, 2, 2, 4)
    assert algebra.lines_are_perpendicular(1, 0, 0, 1)
    assert algebra.line_contains_point(
        *algebra.parallel_line_through_point(1, 2, 3, 4), 3, 4
    )
    assert algebra.line_contains_point(
        *algebra.perpendicular_line_through_point(1, 2, 3, 4), 3, 4
    )

    with pytest.raises(ValueError):
        algebra.line_intersection_general(1, 0, 1, 2, 0, 2)
    with pytest.raises(ValueError):
        algebra.lines_are_parallel(0, 0, 1, 0)


def test_point_line_geometry():
    assert algebra.point_line_distance(0, 1, 0, 3, 4) == 4
    assert algebra.line_point_projection(0, 1, 0, 3, 4) == cs.Cartesian2D(3, 0)
    assert algebra.midpoint(0, 0, 2, 4) == cs.Cartesian2D(1, 2)
    assert algebra.midpoint_from_points(
        a=cs.Cartesian2D(0, 0), b=cs.Cartesian2D(2, 4)
    ) == cs.Cartesian2D(1, 2)

    bisector = algebra.perpendicular_bisector(0, 0, 2, 0)
    assert algebra.line_contains_point(*bisector, 1, 0)
    assert algebra.lines_are_perpendicular(*bisector[:2], 0, 2)

    with pytest.raises(ValueError):
        algebra.perpendicular_bisector(1, 1, 1, 1)


def test_circles_and_line_circle_intersections():
    assert algebra.circle_equation(1, 2, 3) == (-2, -4, -4)
    assert algebra.circle_from_equation(-2, -4, -4) == pytest.approx((1, 2, 3))
    assert algebra.circle_from_three_points(0, 0, 2, 0, 0, 2) == pytest.approx(
        (1, 1, math.sqrt(2))
    )

    intersections = algebra.line_circle_intersection(0, 1, 0, 0, 0, 2)
    assert intersections == [
        cs.Cartesian2D(-2, 0),
        cs.Cartesian2D(2, 0),
    ]
    assert algebra.line_circle_intersection(0, 1, -2, 0, 0, 2) == [cs.Cartesian2D(0, 2)]
    assert algebra.line_circle_intersection(0, 1, -3, 0, 0, 2) == []

    with pytest.raises(ValueError):
        algebra.circle_equation(0, 0, -1)
    with pytest.raises(ValueError):
        algebra.circle_from_equation(0, 0, 1)
    with pytest.raises(ValueError):
        algebra.circle_from_three_points(0, 0, 1, 1, 2, 2)
    with pytest.raises(ValueError):
        algebra.line_circle_intersection(0, 0, 0, 0, 0, 1)
    with pytest.raises(ValueError):
        algebra.line_circle_intersection(0, 1, 0, 0, 0, -1)


def test_vector_point_roundtrip():
    point_2d = cs.Cartesian2D(1, 2)
    restored_2d = algebra.point_from_vector(algebra.vector_from_point(point_2d))
    assert isinstance(restored_2d, cs.Cartesian2D)
    assert (restored_2d.x, restored_2d.y) == (1, 2)

    point_3d = cs.Cartesian3D(1, 2, 3)
    restored_3d = algebra.point_from_vector(algebra.vector_from_point(point_3d))
    assert isinstance(restored_3d, cs.Cartesian3D)
    assert (restored_3d.x, restored_3d.y, restored_3d.z) == (1, 2, 3)


@pytest.mark.parametrize("size", [1, 4])
def test_point_from_vector_rejects_wrong_size(size):
    with pytest.raises(ValueError):
        algebra.point_from_vector(dlx.array([1.0] * size))


@pytest.mark.parametrize(
    "module",
    [algebra, cs, geometry, num_theory, trig],
)
def test_module_exports_are_defined(module):
    for name in module.__all__:
        assert hasattr(module, name)


def test_previously_missing_algebra_exports():
    assert "quadratic_factorized" in algebra.__all__
    assert "vector_from_point" in algebra.__all__
    assert "point_from_vector" in algebra.__all__


def test_trigonometry_does_not_export_internal_helpers():
    assert "parse_expression" not in trig.__all__
    assert "herons_formula" not in trig.__all__
