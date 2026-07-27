"""
The `DuraPy` Constants Library

This module contains all the physical constants used in the `DuraPy` library, such as the gravitational constant, speed of light, and various planetary parameters.
The constants are stored as instances of the `Constant` class, which includes the value, unit, and name of the constant.
"""

# Alpha - A α, Beta - B β,    Gamma - Γ γ,   Delta - Δ δ,   Epsilon - E ε, Zeta - Z ζ, Eta - H η,     Theta - Θ θ,
# Iota - I ι,  Kappa - K κ,   Lambda - Λ λ,  Mu - M μ,      Nu - N ν,      Xi - Ξ ξ,   Omicron - O ο, Pi - Π π,
# Rho - P ρ,   Sigma - Σ σ ς, Tau - T τ,     Ypsilon - Y υ, Phi - Φ φ,     Chi - X χ,  Psi - Ψ ψ,     Omega - Ω ω

# Order: Length, Mass, Time, Electric Charge, Thermodynamic Temperature, Amount of Substance, Luminous Intensity

from fractions import Fraction

from ..shared.numval_types import Constant, Quantity
from .units import (
    AMPERE as _AMPERE,
)
from .units import (
    COULOMB as _COULOMB,
)
from .units import (
    FARAD as _FARAD,
)
from .units import (
    HERTZ as _HERTZ,
)
from .units import (
    JOULE as _JOULE,
)
from .units import (
    KELVIN as _KELVIN,
)
from .units import (
    KILOGRAM as _KILOGRAM,
)
from .units import (
    METER as _METER,
)
from .units import (
    MOLE as _MOLE,
)
from .units import (
    MPS as _MPS,
)
from .units import (
    NEWTON as _NEWTON,
)
from .units import (
    NUMERICAL as _NUM,
)
from .units import (
    OHM as _OHM,
)
from .units import (
    SECOND as _SECOND,
)
from .units import (
    UNIGUNIT as _UNIGUNIT,
)
from .units import (
    VOLT as _VOLT,
)
from .units import (
    WATT as _WATT,
)
from .units import (
    G as _G,
)

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

# Mathematical/Dimensionless Constants
E = Constant(Quantity(2.718281828459045, _NUM), "Eulers Number")
PI = Constant(Quantity(3.141592653589793, _NUM), "Pi - π")
TAU = Constant(Quantity(PI.value * 2, _NUM), "Archimedes' Constant")
INF = Constant(Quantity(float("inf"), _NUM), "Positive Infinity")
NINF = Constant(Quantity(float("-inf"), _NUM), "Negative Infinity")
IMAG = Constant(Quantity(1j, _NUM), "Imaginary Unit - sqrt(-1)")
GOLDEN = Constant(Quantity(1.618033988749895, _NUM), "The Golden Ratio - φ,")
EULMAS = Constant(Quantity(0.5772156649015329, _NUM), "The Euler-Mascheroni Constant")
FSTRUCT = Constant(Quantity(7.2973525693e-03, _NUM), "Fine-Structure Constant")

# Length Constants - L
PLANCKL = Constant(Quantity(1.616255e-35, _METER), "Planck Length")
BOHR_R = Constant(Quantity(5.291772109e-11, _METER), "The Bohr Radius")
EARTH_R = Constant(Quantity(6.371e6, _METER), "Radius of the Earth")
ASTUNIT = Constant(Quantity(1.496e11, _METER), "Astronomical Unit")
MOON_R = Constant(Quantity(1.737e6, _METER), "Radius of the Moon")
SUN_R = Constant(Quantity(6.957e8, _METER), "Radius of the Sun")
MARS_R = Constant(Quantity(3.390e6, _METER), "Radius of Mars")
LIGHTYR = Constant(Quantity(9.461e15, _METER), "Light year")
PARSEC = Constant(Quantity(0.086e16, _METER), "Parsec")

# Mass Constants - M
ELECTRON_M = Constant(Quantity(9.1093837015e-31, _KILOGRAM), "Electron Mass")
NEUTRON_M = Constant(Quantity(1.67492749804e-27, _KILOGRAM), "Neutron Mass")
PROTON_M = Constant(Quantity(1.67262192369e-27, _KILOGRAM), "Proton Mass")
EARTH_M = Constant(Quantity(5.972e24, _KILOGRAM), "Mass of the Earth")
MOON_M = Constant(Quantity(7.342e22, _KILOGRAM), "Mass of the Moon")
MARS_M = Constant(Quantity(6.390e23, _KILOGRAM), "Mass of Mars")
SUN_M = Constant(Quantity(1.989e30, _KILOGRAM), "Mass of the Sun")

# Time Constants - T
PLANCK_T = Constant(Quantity(5.39e-43, _SECOND), "Planck Time")
MINUTE = Constant(Quantity(60, _SECOND), "Minute")
HOUR = Constant(Quantity(3600, _SECOND), "Hour")
DAY = Constant(Quantity(86400, _SECOND), "Day")
YEAR = Constant(Quantity(31536000, _SECOND), "Year")

# Electric Charge Constants - I

# Thermodynamic Temperature Constants - Θ

# Amount of Substance Constants - N

# Luminous Intensity Constants - J

# Gravity Constants - L / T^2
EARTH_G = Constant(Quantity(9.8, _G), "Surface Gravity of the Earth")
MOON_G = Constant(Quantity(1.62, _G), "Surface Gravity of the Moon")
MARS_G = Constant(Quantity(3.71, _G), "Surface Gravity of Mars")
SUN_G = Constant(Quantity(274, _G), "Surface Gravity of the Sun")

# Speed Constants - L / T
C = Constant(Quantity(299792458, _MPS), "Speed of Light")
MACH = Constant(Quantity(343, _MPS), "Speed of Sound at sea level")

# Energy Constants
PLANCK = Constant(Quantity(6.2607015e-34, _JOULE), "Planck's Constant")
PLANCKR = Constant(Quantity(1.054571817e-34, _JOULE), "Reduced Planck Constant")

# Universal Gravitational Constant
UNI_G = Constant(
    Quantity(6.74e-11, _UNIGUNIT), "Gravitational Constant"
)  # L^3 / M * T^2

# Vacuum-related Constants
VAC_PERMEABILITY = Constant(
    Quantity(1.25663706127e-06, _NEWTON / _AMPERE**2), "Vacuum Permeability"
)  # Measure of the resistance encountered when forming a magnetic field in a vacuum; also known as the magnetic constant.
VAC_PERMITTIVITY = Constant(
    Quantity(8.8541878128e-12, _FARAD / _METER), "Vacuum Permittivity"
)  # Capability of a vacuum to permit electric field lines; also known as the electric constant.
VAC_IMPEDANCE = Constant(
    Quantity(376.730313412, _OHM), "Vacuum Impedance"
)  # Ratio of the magnitudes of the electric and magnetic fields in an electromagnetic wave traveling through a vacuum.

# Miscellaneous Constants
STEFAN_BOLTZMANN = Constant(
    Quantity(5.670374419e-08, _WATT / (_METER**2 * _KELVIN**4)),
    "Stefan-Boltzmann Constant"
)  # Constant of proportionality in the Stefan-Boltzmann law relating total energy radiated per unit surface area of a black body.
COULOMB_CONST = Constant(
    Quantity(8.9875517923e09, _NEWTON * _METER**2 / _AMPERE**2), "Coulomb Constant"
)  # Proportionality constant used in electrostatics equations, equal to 1 / (4pi * epsilon_0).
GAS_CONSTANT = Constant(
    Quantity(8.314462618, _JOULE / (_MOLE * _KELVIN)), "Gas Constant"
)  # Work performed by one mole of a gas during a temperature change of 1 Kelvin at constant pressure.
JOSEPHSON = Constant(
    Quantity(483597.8484e09, _HERTZ / _VOLT), "Josephson Constant"
)  # Constant relating the potential difference across a Josephson junction to the frequency of the alternating current.
BOLTZMANN = Constant(
    Quantity(0.380649e-23, _JOULE / _KELVIN), "Boltzmann Constant"
)  # Relates the average relative kinetic energy of particles in a gas with the thermodynamic temperature of the gas.
AVOGADRO = Constant(
    Quantity(6.02214076e23, _MOLE**-1), "Avogadro Constant"
)  # Number of constituent particles (usually atoms or molecules) contained in one mole of a substance.
FARADAY = Constant(
    Quantity(96485.33212, _COULOMB / _MOLE), "Faraday Constant"
)  # Total electric charge carried by one mole of electrons.
RYDBERG = Constant(
    Quantity(10973731.56816, _METER**-1), "Rydberg Constant"
)  # Limiting value of the highest wavenumber of any photon that can be emitted from an atom.
HUBBLE = Constant(
    Quantity(70000, _MPS) / PARSEC, "Hubble Constant"
)  # The average speed of galaxies moving away from each other in the universe -- the expansion rate of the universe.
WIEN = Constant(
    Quantity(2.897771955e-03, _METER * _KELVIN), "Wien Displacement Constant"
)  # Relationship between the thermodynamic temperature of a blackbody and the wavelength of its peak radiation.
