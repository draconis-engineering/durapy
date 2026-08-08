"""Resistor types for the UniPower module."""

from types import MappingProxyType

from ...shared.color_system import ANSI_COLORS
from ...shared.numval_types import Quantity
from ...shared.units import OHM
from ..exceptions import InvalidColors

BANDS: MappingProxyType[str, int] = MappingProxyType(
    {
        "black": 0,
        "brown": 1,
        "red": 2,
        "orange": 3,
        "yellow": 4,
        "green": 5,
        "blue": 6,
        "violet": 7,
        "gray": 8,
        "white": 9,
    }
)
MULTIPLIERS: MappingProxyType[str, float] = MappingProxyType(
    {
        "silver": 0.01,
        "gold": 0.1,
        "black": 1.0,
        "brown": 10.0,
        "red": 100.0,
        "orange": 1000.0,
        "yellow": 10000.0,
        "green": 100000.0,
        "blue": 1000000.0,
        "violet": 10000000.0,
        "gray": 100000000.0,
        "white": 1000000000.0,
    }
)
TOLERANCES: MappingProxyType[str, float] = MappingProxyType(
    {
        "brown": 1.0,
        "red": 2.0,
        "green": 0.5,
        "blue": 0.25,
        "violet": 0.1,
        "gray": 0.05,
        "gold": 5.0,
        "silver": 10.0,
    }
)


def resistor_insight(
    C1: str, C2: str, C3: str, C4: str, C5: str | None = None
) -> tuple[float, float, float, float]:
    """Returns the resistance value of a resistor given its color bands."""

    # Try given colors
    try:
        b1 = BANDS[C1]
        b2 = BANDS[C2]

    # Invalid colors given
    except KeyError as e:
        raise InvalidColors(e) from e

    # 4-color mode
    if C5 is None:
        try:
            multiplier = MULTIPLIERS[C3]
            tolerance = TOLERANCES[C4]
        except KeyError as e:
            raise InvalidColors(e) from e

        ohms = (b1 * 10 + b2) * multiplier

    # C5 given, 5-color mode
    else:
        try:
            b3 = BANDS[C3]
            multiplier = MULTIPLIERS[C4]
            tolerance = TOLERANCES[C5]
        except KeyError as e:
            raise InvalidColors(e) from e

        ohms = (b1 * 100 + b2 * 10 + b3) * multiplier

    tolerance_decimal = tolerance / 100

    lower = ohms * (1 - tolerance_decimal)
    upper = ohms * (1 + tolerance_decimal)

    return ohms, tolerance, lower, upper


class Resistor:
    """Resistor class that represents a resistor with color bands and ohms value."""

    def __init__(self, colors: tuple[str, str, str, str, str | None]) -> None:
        self._ohms, self.tolerance, self.lower, self.upper = resistor_insight(*colors)
        self.c_1, self.c_2, self.c_3, self.c_4, self.c_5 = colors

    def __repr__(self) -> str:
        return f"Resistor(ohms={self._ohms}, tolerance={self.tolerance}, lower={self.lower}, upper={self.upper})"

    def __str__(self) -> str:
        return f"{self._ohms} ohms +- {self.tolerance}% \n Low: {self.lower} High: {self.upper}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Resistor):
            return False
        return (
            self._ohms == other._ohms
            and self.tolerance == other.tolerance
            and self.lower == other.lower
            and self.upper == other.upper
        )

    @property
    def ohms(self) -> Quantity:
        return Quantity(self._ohms, OHM)

    @property
    def color_code(self) -> tuple[str, str, str, str, str | None]:
        return self.c_1, self.c_2, self.c_3, self.c_4, self.c_5

    def visualize(self) -> str:
        """Prints a ASCII representation of a resistor with the color code"""

        def block(color: str):
            ansi = ANSI_COLORS.get(color.lower(), "\033[0m")
            reset = "\033[0m"
            return f"{ansi}    {reset}"

        if self.c_5:
            return f"    <----------------------------->\n    |                             |\n    |  ┌────┬────┬────┬────┬────┐ |\n   ----│{block(self.c_1)}│{block(self.c_2)}│{block(self.c_3)}│{block(self.c_4)}│{block(self.c_5)}|----\n    |  └────┴────┴────┴────┴────┘ |\n    |                             |\n    <----------------------------->"
        return f"    <------------------------->\n    |                         |\n    |  ┌────┬────┬────┬────┐  |\n   ----│{block(self.c_1)}│{block(self.c_2)}│{block(self.c_3)}│{block(self.c_4)}│----\n    |  └────┴────┴────┴────┘  |\n    |                         |\n    <------------------------->"
