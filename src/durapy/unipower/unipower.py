"""`UniPower` source"""

import math
from types import MappingProxyType

from ..shared.constants import PI
from ..shared.numval_types import Quantity
from ..shared.units import FARAD, OHM, SECOND, VOLT, WATT

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


def ohms_law(
    v: float | None = None, i: float | None = None, r: float | None = None
) -> tuple[float, float, float]:
    """Ohms Law calculation for voltage, current, and resistivity. Returns: (V, I, R)"""

    # Find missing parameters
    missing = [
        param for param, value in zip(("v", "i", "r"), (v, i, r)) if value is None
    ]

    if v is None:
        if i is None or r is None:
            raise TypeError(ohms_law, missing)
        v = i * r

    elif i is None:
        if r is None:
            raise TypeError(ohms_law, missing)
        i = v / r

    elif r is None:
        r = v / i

    return v, i, r


def volt_divider(v_in: float, r_1: float, r_2: float) -> Quantity:
    """Calculates the output voltage of a voltage divider from input voltage and the two resistances."""
    return Quantity((v_in * (r_2 / (r_1 + r_2))), VOLT)


def rc_time_constant(capacitance: float, resistance: float) -> Quantity:
    """Calculates the time constant of an RC circuit from capacitance in farads and resistance in ohms."""
    return Quantity((capacitance * resistance), SECOND)


def inductor_impedance(hertz: float, inductance: float) -> Quantity:
    """Calculates the impedance of an inductor at a given frequency in hertz and inductance in henrys."""
    return Quantity((2 * PI * hertz * inductance), OHM)


def power_dissipation(
    v: float | None = None, i: float | None = None, r: float | None = None
) -> Quantity:
    """Calculates power dissipation from voltage, current and resistance. If all three parameters are given, it checks for consistency between the three formulas P = I^2 * R, P = V^2 / R and P = V * I."""

    # Find missing parameters
    missing = [
        param for param, value in zip(("v", "i", "r"), (v, i, r)) if value is None
    ]

    if v is None:
        if i is None or r is None:  # Too many missing arguments
            raise TypeError(power_dissipation, missing)
        return Quantity(i**2 * r, WATT)

    elif i is None:
        if r is None:  # Too many missing arguments
            raise TypeError(power_dissipation, missing)
        return Quantity(v**2 / r, WATT)

    elif (
        r is None
    ):  # If V or I was none, the earlier if/elif chains would've tripped, so no raising required
        return Quantity(v * i, WATT)

    # All parameters given - Check for consistency
    else:
        P1 = i**2 * r
        P2 = v**2 / r
        P3 = v * i

        # P1 != P2
        if not math.isclose(P1, P2):
            # P1 != P3 -> Error with P1
            if not math.isclose(P1, P3):
                raise ValueError("Inconsistency with P1 = I ** 2 * R")
            # P1 == P3 -> Error with P2
            else:
                raise ValueError("Inconsistency with P2 = V ** 2 / R")

        # P1 == P2
        else:
            # P2 != P3 -> Error with P3
            if not math.isclose(P2, P3):
                raise ValueError("Inconsistency with P3 = V * I")
            # P1 == P2 == P3 -> All formulas agree
            else:
                return Quantity(math.fsum([P1, P2, P3]) / 3, WATT)


def total_esr(caps: list[tuple[float, float, float]], connection: str) -> Quantity:
    """Calculates total ESR of a list of capacitors based on their connection type. Caps are in the format (capacitance, voltage, esr) for now."""
    if connection == "series":
        return Quantity(math.fsum(cap[2] for cap in caps), OHM)

    if connection == "parallel":
        try:
            return Quantity(
                1 / math.fsum(1 / cap[2] for cap in caps if cap[2] != 0), OHM
            )
        except ZeroDivisionError:
            return Quantity(0, OHM)

    raise ValueError("Connection type must be 'parallel' or 'series'")


def total_capacitance(
    caps: list[tuple[float, float, float]], connection: str
) -> tuple[
    Quantity, Quantity, Quantity
]:  ### caps (capacitance, voltage, esr) (for now)
    """Calculates total capacitance, voltage limit and ESR of a list of capacitors based on their connection type."""

    if connection == "parallel":
        total_capacitance = math.fsum(cap[0] for cap in caps)
        volt_limit = min([cap[1] for cap in caps])
        return (
            Quantity(total_capacitance, FARAD),
            Quantity(volt_limit, VOLT),
            Quantity(total_esr(caps, connection), OHM),
        )

    if connection == "series":
        total_capacitance = 1 / math.fsum(1 / cap[0] for cap in caps)
        volt_limit = math.fsum([cap[1] for cap in caps])
        return (
            Quantity(total_capacitance, FARAD),
            Quantity(volt_limit, VOLT),
            Quantity(total_esr(caps, connection), OHM),
        )

    raise ValueError("Connection type must be 'parallel' or 'series'")
