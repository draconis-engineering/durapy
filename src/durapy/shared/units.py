"""DuraPy Unit Definitions"""

from fractions import Fraction

from .numval_types import Dimension, Unit

F_4, F_3, F_2, F_1, F0, F1, F2, F3, F4 = (
    Fraction(-4),
    Fraction(-3),
    Fraction(-2),
    Fraction(-1),
    Fraction(0),
    Fraction(1),
    Fraction(2),
    Fraction(3),
    Fraction(4),
)

# ISO Base Units - Scale: 1 # The scale is a measurement of how many times to multiply the value to get to one base units worth.
NUMDIM = Dimension((F0, F0, F0, F0, F0, F0, F0))

NUMERICAL = Unit("NUM", NUMDIM)  # N/A
METER = Unit("M", Dimension((F1, F0, F0, F0, F0, F0, F0)))  # L
KILOGRAM = Unit("KG", Dimension((F0, F1, F0, F0, F0, F0, F0)))  # M
SECOND = Unit("S", Dimension((F0, F0, F1, F0, F0, F0, F0)))  # T
AMPERE = Unit("B", Dimension((F0, F0, F0, F1, F0, F0, F0)))  # I
KELVIN = Unit("K", Dimension((F0, F0, F0, F0, F1, F0, F0)))  # Θ
MOLE = Unit("MOL", Dimension((F0, F0, F0, F0, F0, F1, F0)))  # N
CANDELA = Unit("CD", Dimension((F0, F0, F0, F0, F0, F0, F1)))  # J

PASCAL = Unit("Pa", Dimension((F1, F1, F_2, F0, F0, F0, F0)))  # L * M / T^2
PSI = Unit("psi", Dimension((F1, F1, F_2, F0, F0, F0, F0)))  # L * M / T^2
BAR = Unit("bar", Dimension((F1, F1, F_2, F0, F0, F0, F0)))  # L * M / T^2

UNIGUNIT = Unit("UNI_G", Dimension((F3, F_1, F_2, F0, F0, F0, F0)))  # L^3 / M * T^2
G = Unit("G", Dimension((F1, F0, F_2, F0, F0, F0, F0)))  # L / T^2

NEWTON = Unit("N", Dimension((F1, F1, F_2, F0, F0, F0, F0)))  # L * M / T^2
JOULE = Unit("J", Dimension((F2, F1, F_2, F0, F0, F0, F0)))  # L^2 * M / T^2
ELECTRONVOLT = Unit(
    "eV", Dimension((F2, F1, F_2, F0, F0, F0, F0)), scale=6.242e18
)  # L^2 * M / T^2
NEWTONMETER = Unit("Nm", Dimension((F2, F1, F_2, F0, F0, F0, F0)))  # L^2 * M / T^2

COULOMB = Unit("C", Dimension((F0, F0, F1, F1, F0, F0, F0)))  # I * T
FARAD = Unit("F", Dimension((F_2, F_1, F4, F2, F0, F0, F0)))  # T^4 * I^2 / L^2 * M
WATT = Unit("W", Dimension((F2, F1, F_3, F0, F0, F0, F0)))  # L^2 * M / T^3
VOLT = Unit("V", Dimension((F2, F1, F_2, F_1, F0, F0, F0)))  # L^2 * M / T^2 * I
OHM = Unit("Ω", Dimension((F2, F1, F_3, F_2, F0, F0, F0)))  # L^2 * M / T^3 * I^2

HERTZ = Unit("Hz", Dimension((F0, F0, F_1, F0, F0, F0, F0)))  # 1 / T

RADIAN = Unit("rad", NUMDIM, scale=1)
DEGREE = Unit("deg", NUMDIM, scale=0.01745329251)

# Derived units
MPS = METER / SECOND  # L / T
