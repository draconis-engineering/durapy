"""Safe parsing of user-supplied mathematical expressions.

``sympy.sympify`` evaluates its input and can therefore run arbitrary Python
code (for example ``__import__('os').getcwd()``).  The helpers in this module
only accept a small, explicitly whitelisted subset of mathematical syntax so
that expression strings coming from users cannot escape the sandbox.
"""

from __future__ import annotations

import re

import sympy
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

# Names a user may reference in an expression.  Everything else is rejected
# before the expression is evaluated.  Keep this list deliberately small.
_ALLOWED_NAMES: frozenset[str] = frozenset(
    {
        "x",
        # constants (``e``/``E`` are also needed for scientific notation)
        "e",
        "E",
        "pi",
        # trigonometric
        "sin",
        "cos",
        "tan",
        "cot",
        "sec",
        "csc",
        "asin",
        "acos",
        "atan",
        "acot",
        "sinh",
        "cosh",
        "tanh",
        "asinh",
        "acosh",
        "atanh",
        # exponential / logarithmic
        "exp",
        "log",
        "ln",
        "sqrt",
        "cbrt",
        # misc
        "Abs",
        "abs",
        "sign",
        "floor",
        "ceil",
        "factorial",
        "gamma",
    }
)

_SAFE_GLOBALS: dict[str, object] = {
    # An explicit empty ``__builtins__`` stops Python's ``eval`` from injecting
    # the real builtins when it evaluates the parsed expression.
    "__builtins__": {},
    "Symbol": sympy.Symbol,
    "Integer": sympy.Integer,
    "Float": sympy.Float,
    "Rational": sympy.Rational,
    "Pow": sympy.Pow,
    "e": sympy.E,
    "E": sympy.E,
    "pi": sympy.pi,
    "sin": sympy.sin,
    "cos": sympy.cos,
    "tan": sympy.tan,
    "cot": sympy.cot,
    "sec": sympy.sec,
    "csc": sympy.csc,
    "asin": sympy.asin,
    "acos": sympy.acos,
    "atan": sympy.atan,
    "acot": sympy.acot,
    "sinh": sympy.sinh,
    "cosh": sympy.cosh,
    "tanh": sympy.tanh,
    "asinh": sympy.asinh,
    "acosh": sympy.acosh,
    "atanh": sympy.atanh,
    "exp": sympy.exp,
    "log": sympy.log,
    "ln": sympy.log,
    "sqrt": sympy.sqrt,
    "cbrt": sympy.cbrt,
    "Abs": sympy.Abs,
    "abs": sympy.Abs,
    "sign": sympy.sign,
    "floor": sympy.floor,
    "ceil": sympy.ceiling,
    "factorial": sympy.factorial,
    "gamma": sympy.gamma,
}

_TRANSFORMATIONS = standard_transformations + (
    convert_xor,
    implicit_multiplication_application,
)

_NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
# Deliberately excludes quotes, brackets, braces, colons, semicolons and
# backslashes; those are never needed in a plain mathematical expression.
_ALLOWED_CHARS_RE = re.compile(r"^[0-9A-Za-z_\s+\-*/^().,]+$")
_MAX_EXPRESSION_LENGTH = 2000


class UnsafeExpressionError(ValueError):
    """Raised when an expression contains unsupported or unsafe syntax."""


def parse_expression(expression: str) -> sympy.Expr:
    """Parse ``expression`` into a SymPy object without executing Python code.

    Only the names in :data:`_ALLOWED_NAMES` are permitted; anything that
    looks like attribute access, a call to an unknown name, or an import is
    rejected with :class:`UnsafeExpressionError`.
    """
    if not isinstance(expression, str):
        raise TypeError("expression must be a string")
    if not expression.strip():
        raise UnsafeExpressionError("expression must not be empty")
    if len(expression) > _MAX_EXPRESSION_LENGTH:
        raise UnsafeExpressionError("expression is too long")
    if not _ALLOWED_CHARS_RE.match(expression):
        raise UnsafeExpressionError("expression contains unsupported characters")

    for name in _NAME_RE.findall(expression):
        if name not in _ALLOWED_NAMES:
            raise UnsafeExpressionError(f"unsupported name in expression: {name!r}")

    return parse_expr(
        expression,
        local_dict={"x": sympy.Symbol("x")},
        global_dict=dict(_SAFE_GLOBALS),
        transformations=_TRANSFORMATIONS,
    )
