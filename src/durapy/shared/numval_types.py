"""The `Constant`, `Quantity`, `Dimension` and `Unit` classes represent physical quantities with values and dimensions."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


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
        return Dimension(tuple(Fraction(base**x) for x in self.exponents))


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
        return Unit(
            symbol=self.symbol,
            dimension=base**self.dimension,
            scale=base**self.scale,
        )


# The 7 SI Base symbols mapping to your 7-tuple indices
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


def get_symbol(quantity: Quantity) -> str:
    """Dynamic construction of a string from base elements (e.g., m·kg·s⁻²)"""

    # Iterate over base symbols and exponents to build the symbol string
    positives = []
    negatives = []

    # Iterate over base symbols and exponents to build the symbol string
    for symbol, exp in zip(BASE_SYMBOLS, quantity.unit.dimension):
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
    return tuple(Fraction(exp) for exp in symbol.replace("·", "").split("⁻") if exp)


class Quantity:
    """Quantity class for representing quantities with dimensions and symbols."""

    def __init__(self, value: complex | Quantity, unit: Unit) -> None:

        # Handle Quantity input
        if isinstance(value, Quantity):
            self._value = value._value
            self.unit = unit if unit else value.unit

        # Handle float/complex input
        else:
            self._value = value
            self.unit = unit

    @property
    def value(self) -> float:
        return self._value.real

    @property
    def imagvalue(self) -> float:
        return self._value.imag

    def __repr__(self) -> str:
        return f"Quantity({self._value!r}, {self.unit!r})"

    def __str__(self) -> str:
        return f"{self._value} {self.unit.symbol}"

    def __abs__(self) -> Quantity:
        return Quantity(abs(self._value), self.unit)

    def __neg__(self) -> Quantity:
        return Quantity(-self._value, self.unit)

    def __add__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            raise TypeError("Cannot add a Quantity to a scalar.")
        if self.unit != other.unit:
            raise ValueError(f"Unit mismatch: {self.unit} vs {other.unit}")
        return Quantity(self._value + other._value, self.unit)

    def __sub__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            raise TypeError("Cannot subtract a Quantity from a scalar.")
        if self.unit != other.unit:
            raise ValueError(f"Unit mismatch: {self.unit} vs {other.unit}")
        return Quantity(self._value - other._value, self.unit)

    def __mul__(self, other: float | Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            return Quantity(self._value * other, self.unit)
        newunit = self.unit * other.unit
        return Quantity(self._value * other._value, newunit)

    def __rmul__(self, other: float) -> Quantity:
        return self.__mul__(other)  # Commutative

    def __truediv__(self, other: Quantity | float) -> Quantity:
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, self.unit / other.unit)
        if isinstance(other, (int, float)):
            return Quantity(self._value / other, self.unit)
        raise TypeError(f"Cannot divide Quantity by {type(other)}")

    def __rtruediv__(self, other: Quantity | float) -> Quantity:
        if not isinstance(other, Quantity):
            return Quantity(other / self._value, -self.unit)
        return other.__truediv__(self)

    def __pow__(self, power: Quantity | float) -> Quantity:
        if not isinstance(power, (int, float)):
            raise TypeError("Power must be a scalar number.")
        new_dims = self.unit**power
        return Quantity(self._value**power, new_dims)

    def __rpow__(self, other: Quantity | float) -> Quantity:
        if isinstance(other, Quantity):
            return Quantity(
                other._value**self._value, self.unit
            )  # What about unit change?
        else:
            return Quantity(other**self._value, self.unit)

    def __int__(self) -> int:
        return int(self._value.real)

    def __float__(self) -> float:
        return float(self._value.real)

    def __complex__(self) -> complex:
        return complex(self._value, 0)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Quantity):
            return self.unit == value.unit and self._value == value._value
        if isinstance(value, (int, float)):
            return self._value == value
        return NotImplemented

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __ge__(self, other: float | Quantity) -> bool:
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                raise ValueError(
                    f"Cannot compare units of different dimensions: {self.unit} vs {other.unit}"
                )
            return self._value.real >= other._value.real
        return NotImplemented

    def __gt__(self, other: float | Quantity) -> bool:
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                raise ValueError(
                    f"Cannot compare units of different dimensions: {self.unit} vs {other.unit}"
                )
            return self._value.real > other._value.real
        return NotImplemented

    def __le__(self, other: float | Quantity) -> bool:
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                raise ValueError(
                    f"Cannot compare units of different dimensions: {self.unit} vs {other.unit}"
                )
            return self._value.real <= other._value.real
        return NotImplemented

    def __lt__(self, other: float | Quantity) -> bool:
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                raise ValueError(
                    f"Cannot compare units of different dimensions: {self.unit} vs {other.unit}"
                )
            return self._value.real < other._value.real
        return NotImplemented


@dataclass(frozen=True)
class Constant(Quantity):
    quantity: Quantity
    name: str

    def __int__(self) -> int:
        return int(self.quantity)

    def __float__(self) -> float:
        return float(self.quantity)

    def __complex__(self) -> complex:
        return complex(self.quantity)

    @property
    def value(self) -> float:
        return self.quantity._value.real

    @property
    def unit(self) -> Unit:
        return self.quantity.unit
