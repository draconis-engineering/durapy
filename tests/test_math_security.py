"""Security regression tests for user-supplied expression parsing.

Historically ``sympy.sympify`` was used directly on user input, which allows
arbitrary Python execution (e.g. ``__import__('os').getcwd()``).  These tests
pin the restricted parser in place.
"""

import pytest
import sympy

from durapy.uniCLI import unicli
from durapy.unimath import algebra, trigonometry
from durapy.unimath._parsing import UnsafeExpressionError, parse_expression

# Payloads that must never reach ``eval``.  ``getcwd`` is used as a harmless
# canary: if the sandbox is bypassed the call succeeds instead of raising.
MALICIOUS_EXPRESSIONS = [
    "__import__('os').getcwd()",
    '__import__("os").getcwd()',
    "os.system('id')",
    "x.__class__",
    "(1).__class__.__bases__",
    "eval('1+1')",
    "open('/etc/passwd')",
    "x; import os",
    "x[0]",
    "x`whoami`",
]


@pytest.mark.parametrize("payload", MALICIOUS_EXPRESSIONS)
def test_parse_expression_rejects_python_code(payload):
    with pytest.raises(UnsafeExpressionError):
        parse_expression(payload)


def test_parse_expression_rejects_overlong_input():
    with pytest.raises(UnsafeExpressionError):
        parse_expression("x + " * 1000 + "x")


@pytest.mark.parametrize(
    "expression",
    [
        "x**2 + 2*x + 1",
        "sin(x)",
        "cos(x) + tan(x)",
        "sqrt(x)",
        "2x",
        "x^2",
        "1e-5*x",
        "E**x",
        "pi*x",
        "exp(-x)",
    ],
)
def test_parse_expression_accepts_math(expression):
    assert isinstance(parse_expression(expression), sympy.Basic)


def test_derivative_still_works():
    assert sympy.simplify(algebra.derivative("x**2") - 2 * sympy.Symbol("x")) == 0
    assert algebra.derivative("x**3", x=2) == pytest.approx(12.0, rel=1e-4)


def test_derivative_rejects_code_execution():
    with pytest.raises(UnsafeExpressionError):
        algebra.derivative("__import__('os').getcwd()")


def test_tangent_formula_rejects_code_execution():
    with pytest.raises(UnsafeExpressionError):
        trigonometry.tangent_formula("__import__('os').getcwd()", "x")


def test_cubic_helpers_still_work():
    assert sorted(algebra.cubic_zeros(1, 0, -1, 0)) == [-1, 0, 1]
    vertices = algebra.cubic_vertex(1, 0, -3, 0)
    assert sorted(x for x, _ in vertices) == [-1, 1]


def test_clear_terminal_does_not_shell_out(monkeypatch):
    called = {}

    def fake_clear(self):
        called["cleared"] = True

    monkeypatch.setattr(unicli.RichConsole, "clear", fake_clear)
    unicli.clear_terminal()
    assert called.get("cleared") is True
