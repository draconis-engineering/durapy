"""Decorators for mathematical operations on matrices and vectors."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any

from .exceptions import NonSquareShapeError


def requires_square(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that requires the matrix to be square."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_square():
            raise NonSquareShapeError(self.shape)
        return func(self, *args, **kwargs)

    return wrapper


def requires_real(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that requires the vector to be real (no complex numbers)."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if any(isinstance(component, complex) for component in self.components):
            raise ValueError("Complex numbers are not supported")
        return func(self, *args, **kwargs)

    return wrapper
