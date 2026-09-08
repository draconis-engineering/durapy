"""The `Constant`, `Quantity`, `Dimension` and `Unit` classes represent physical quantities with values and dimensions."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import override


@dataclass(frozen=True, slots=True)
class Dimension:
    exponents: tuple[Fraction, ...]

    def __iter__(self):
        return iter(self.exponents)

    def __neg__(self) -> Dimension:
        return Dimension(tuple(-x for x in self.exponents))

    def __mul__(self, other: Dimension) -> Dimension:
        return Dimension(
            tuple(Fraction(a + b) for a, b in zip(self.exponents, other.exponents))
        )

    def __rmul__(self, other: Dimension) -> Dimension:
        return Dimension(
            tuple(Fraction(a + b) for a, b in zip(self.exponents, other.exponents))
        )

    def __truediv__(self, other: Dimension) -> Dimension:
        return Dimension(
            tuple(Fraction(a - b) for a, b in zip(self.exponents, other.exponents))
        )

    def __rtruediv__(self, other: Dimension) -> Dimension:
        return Dimension(
            tuple(Fraction(b - a) for a, b in zip(self.exponents, other.exponents))
        )

    def __pow__(self, power: float | Fraction) -> Dimension:
        return Dimension(tuple(Fraction(power) * x for x in self.exponents))

    def __rpow__(self, base: float) -> Dimension:
        raise TypeError("Exponentiation of base by Dimension is not physically meaningful")


@dataclass(frozen=True, slots=True)
class Unit:
    symbol: str
    dimension: Dimension
    scale: float = 1.0

    def __neg__(self) -> Unit:
        return Unit(
            symbol=f"-{self.symbol}",
            dimension=-self.dimension,
            scale=-self.scale,
        )

    def __mul__(self, other: Unit) -> Unit:
        return Unit(
            symbol=f"{self.symbol}·{other.symbol}",
            dimension=self.dimension * other.dimension,
            scale=self.scale * other.scale,
        )

    def __rmul__(self, other: Unit) -> Unit:
        return Unit(
            symbol=f"{other.symbol}·{self.symbol}",
            dimension=other.dimension * self.dimension,
            scale=other.scale * self.scale,
        )

    def __truediv__(self, other: Unit) -> Unit:
        return Unit(
            symbol=f"{self.symbol}/{other.symbol}",
            dimension=self.dimension / other.dimension,
            scale=self.scale / other.scale,
        )

    def __rtruediv__(self, other: Unit) -> Unit:
        return Unit(
            symbol=f"{other.symbol}/{self.symbol}",
            dimension=other.dimension / self.dimension,
            scale=other.scale / self.scale,
        )

    def __pow__(self, power: float | Fraction) -> Unit:
        return Unit(
            symbol=self.symbol,
            dimension=self.dimension**power,
            scale=self.scale**power,
        )

    def __rpow__(self, base: float) -> Unit:
        raise TypeError("Exponentiation of base by Unit is not physically meaningful")


# The 7 SI Base symbols mapping to 7-tuple indices
BASE_SYMBOLS = ["m", "kg", "s", "A", "K", "mol", "cd"]
SUPERSCRIPTS = {
    "-": "⁻",
    "0": "⁰",
    "1": "",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
}


def format_exponent(exp: Fraction) -> str:
    """Converts a number like -2 into a superscript string like ⁻²."""
    # Handle ints cleanly so 2.0 becomes ² instead of ².⁰
    val_str = str(int(exp)) if exp.is_integer() else str(exp)
    if val_str == "1":
        return ""
    return "".join(SUPERSCRIPTS.get(char, char) for char in val_str)


def _unwrap_quantity(q: Quantity) -> Quantity:
    """Unwrap Constant to its underlying Quantity for internal operations."""
    # Avoid circular import: check for 'quantity' attribute that Constants have
    if hasattr(q, "quantity") and hasattr(q, "name"):
        try:
            return q.quantity  # type: ignore
        except Exception:
            pass
    return q


def get_symbol(quantity: Quantity) -> str:
    """Dynamic construction of a string from base elements (e.g., m·kg·s⁻²)"""
    q = _unwrap_quantity(quantity)
    # Iterate over base symbols and exponents to build the symbol string
    positives: list[str] = []
    negatives: list[str] = []

    # Iterate over base symbols and exponents to build the symbol string
    for symbol, exp in zip(BASE_SYMBOLS, q._unit.dimension):
        if exp == 0:
            continue
        elif exp > 0:
            positives.append(f"{symbol}{format_exponent(exp)}")
        else:
            negatives.append(f"{symbol}{format_exponent(exp)}")

    # Combine them cleanly, positive first, then negative. Example output format: m·kg·s⁻²
    parts = positives + negatives
    return "·".join(parts) if parts else ""


def symbol_to_dimensions(symbol: str) -> tuple[Fraction, ...]:
    """Returns the dimensions as a tuple of exponents from the symbol."""
    # Deprecated stub: kept for backwards compatibility, returns empty tuple.
    # Proper parsing would require a full SI parser.
    return tuple()


class Quantity:
    """Quantity class for representing quantities with dimensions and symbols."""

    def __init__(self, value: complex | Quantity, unit: Unit) -> None:

        self._value: int | float | complex
        self._unit: Unit

        # Handle Quantity/Constant input — unwrap Constant to its Quantity
        if isinstance(value, Quantity):
            unwrapped = _unwrap_quantity(value)  # type: ignore
            # Access private attrs safely for both Quantity and Constant
            src_val = getattr(unwrapped, "_value", None)
            src_unit = getattr(unwrapped, "_unit", None)
            if src_val is None:
                # Fallback for Constant subclass edge: use quantity field
                src_val = unwrapped._value if hasattr(unwrapped, "_value") else value  # type: ignore
            self._value = src_val  # type: ignore
            self._unit = unit if unit is not None else src_unit  # type: ignore
            if self._unit is None:
                raise ValueError("Unit must be provided for Quantity")

        # Handle float/complex input
        else:
            self._value = value
            self._unit = unit

    @property
    def value(self) -> float:
        return self._value.real

    @property
    def imagvalue(self) -> float:
        return self._value.imag

    def __repr__(self) -> str:
        return f"Quantity({self._value!r}, {self._unit!r})"

    def __str__(self) -> str:
        return f"{self._value} {self._unit.symbol}"

    def __abs__(self) -> Quantity:
        return Quantity(abs(self._value), self._unit)

    def __neg__(self) -> Quantity:
        return Quantity(-self._value, self._unit)

    def __add__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            raise TypeError("Cannot add a Quantity to a scalar.")
        other_q = _unwrap_quantity(other)
        if self._unit != other_q._unit:
            raise ValueError(f"Unit mismatch: {self._unit} vs {other_q._unit}")
        return Quantity(self._value + other_q._value, self._unit)

    def __sub__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            raise TypeError("Cannot subtract a Quantity from a scalar.")
        other_q = _unwrap_quantity(other)
        if self._unit != other_q._unit:
            raise ValueError(f"Unit mismatch: {self._unit} vs {other_q._unit}")
        return Quantity(self._value - other_q._value, self._unit)

    def __mul__(self, other: float | Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            return Quantity(self._value * other, self._unit)
        other_q = _unwrap_quantity(other)
        newunit = self._unit * other_q._unit
        return Quantity(self._value * other_q._value, newunit)

    def __rmul__(self, other: float) -> Quantity:
        if isinstance(other, Quantity):
            other_q = _unwrap_quantity(other)
            newunit = other_q._unit * self._unit
            return Quantity(other_q._value * self._value, newunit)
        return Quantity(self._value * other, self._unit)

    def __truediv__(self, other: Quantity | float | int) -> Quantity:
        if isinstance(other, Quantity):
            other_q = _unwrap_quantity(other)
            return Quantity(self._value / other_q._value, self._unit / other_q._unit)
        if isinstance(other, (int, float, complex)):
            return Quantity(self._value / other, self._unit)
        raise TypeError(f"Cannot divide Quantity by {type(other)}")

    def __rtruediv__(self, other: Quantity | float) -> Quantity:
        if not isinstance(other, Quantity):
            # scalar / Quantity -> invert dimensions
            inv_unit = Unit(
                symbol=f"1/{self._unit.symbol}",
                dimension=-self._unit.dimension,
                scale=1.0 / self._unit.scale if self._unit.scale != 0 else float("inf"),
            )
            return Quantity(other / self._value, inv_unit)
        other_q = _unwrap_quantity(other)
        return Quantity(other_q._value / self._value, other_q._unit / self._unit)

    def __pow__(self, power: Quantity | float) -> Quantity:
        if isinstance(power, Quantity):
            raise TypeError("Power must be a scalar number, not a Quantity")
        if not isinstance(power, (int, float, complex)):
            raise TypeError("Power must be a scalar number.")
        new_dims = self._unit**power
        return Quantity(self._value**power, new_dims)

    def __rpow__(self, other: Quantity | float) -> Quantity:
        raise TypeError("Exponentiation with Quantity as exponent is not physically meaningful")

    def __int__(self) -> int:
        return int(self._value.real)

    def __float__(self) -> float:
        return float(self._value.real)

    def __complex__(self) -> complex:
        return complex(self._value, 0)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Quantity):
            other_q = _unwrap_quantity(value)
            return self._unit == other_q._unit and self._value == other_q._value
        if isinstance(value, (int, float, complex)):
            return self._value == value
        return NotImplemented

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __ge__(self, other: float | Quantity) -> bool:
        if isinstance(other, Quantity):
            if self._unit != other._unit:
                raise ValueError(
                    f"Cannot compare units of different dimensions: {self._unit} vs {other._unit}"
                )
            return self._value.real >= other._value.real
        return NotImplemented

    def __gt__(self, other: float | Quantity) -> bool:
        if isinstance(other, Quantity):
            if self._unit != other._unit:
                raise ValueError(
                    f"Cannot compare units of different dimensions: {self._unit} vs {other._unit}"
                )
            return self._value.real > other._value.real
        return NotImplemented

    def __le__(self, other: float | Quantity) -> bool:
        if isinstance(other, Quantity):
            if self._unit != other._unit:
                raise ValueError(
                    f"Cannot compare units of different dimensions: {self._unit} vs {other._unit}"
                )
            return self._value.real <= other._value.real
        return NotImplemented

    def __lt__(self, other: float | Quantity) -> bool:
        if isinstance(other, Quantity):
            if self._unit != other._unit:
                raise ValueError(
                    f"Cannot compare units of different dimensions: {self._unit} vs {other._unit}"
                )
            return self._value.real < other._value.real
        return NotImplemented


@dataclass(frozen=True)
class Constant(Quantity):
    quantity: Quantity
    name: str

    def __post_init__(self):
        # Mirror Quantity's private attrs so Quantity operations work on Constants
        object.__setattr__(self, "_value", self.quantity._value)
        object.__setattr__(self, "_unit", self.quantity._unit)

    def __int__(self) -> int:
        return int(self.quantity)

    def __float__(self) -> float:
        return float(self.quantity)

    def __complex__(self) -> complex:
        return complex(self.quantity)

    @property
    @override
    def value(self) -> float:
        return self.quantity._value.real

    @property
    @override
    def unit(self) -> Unit:
        return self.quantity._unit

    def __repr__(self) -> str:
        return f"Constant({self.quantity!r}, {self.name!r})"

    def __str__(self) -> str:
        return f"{self.quantity._value} {self.quantity._unit.symbol} [{self.name}]"
