"""`UniPhys` thermodynamics source"""

from ..shared.constants import GAS_CONSTANT
from ..shared.numval_types import Quantity
from ..shared.units import JOULE, KELVIN, MOLE, PASCAL


def work(force: float, distance: float) -> float:
    """
    Calculate the work done given force and distance.

    Parameters
    ----------
        force (float): The force applied (in newtons).
        distance (float): The distance over which the force is applied (in meters).

    Returns
    -------
        float: The work done (in joules).
    """
    return force * distance


def entropy(heat: float, temperature: float) -> Quantity:
    """
    Calculate the change in entropy given heat and temperature.

    Parameters
    ----------
        heat (float): The amount of heat transferred (in joules).
        temperature (float): The absolute temperature at which the heat transfer occurs (in kelvin).

    Returns
    -------
        float: The change in entropy (in joules per kelvin).
    """
    if temperature <= 0:
        raise ValueError("Temperature must be greater than zero.")

    return Quantity(heat / temperature, JOULE / KELVIN)


def heat_capacity(mass: float, specific_heat: float) -> float:
    """
    Calculates the heat capacity of a substance given its mass and specific heat.

    Parameters
    ----------
        mass (float): The mass of the substance (in kilograms).
        specific_heat (float): The specific heat capacity of the substance (in joules per kilogram per kelvin).

    Returns
    -------
        float: The heat capacity (in joules per kelvin).
    """
    return mass * specific_heat


def ideal_gas_law(pressure: float, volume: float, temperature: float) -> Quantity:
    """
    Calculate the number of moles of an ideal gas given pressure, volume, and temperature.

    Parameters
    ----------
        pressure (float): The pressure of the gas (in pascals).
        volume (float): The volume of the gas (in cubic meters).
        temperature (float): The absolute temperature of the gas (in kelvin).

    Returns
    -------
        float: The number of moles of the gas.
    """
    return Quantity((pressure * volume) / (GAS_CONSTANT * temperature), MOLE)


def internal_energy(heat: float, work: float) -> float:
    """
    Calculate the change in internal energy given heat and work.

    Parameters
    ----------
        heat (float): The amount of heat transferred to the system (in joules).
        work (float): The amount of work done on the system (in joules).

    Returns
    -------
        float: The change in internal energy (in joules).
    """
    return heat + work


def gibbs_free_energy(enthalpy: float, entropy: float, temperature: float) -> float:
    """
    Calculate the Gibbs free energy given enthalpy, entropy, and temperature.

    Parameters
    ----------
        enthalpy (float): The enthalpy of the system (in joules).
        entropy (float): The entropy of the system (in joules per kelvin).
        temperature (float): The absolute temperature (in kelvin).

    Returns
    -------
        float: The Gibbs free energy (in joules).
    """
    return enthalpy - temperature * entropy


def carnot_efficiency(temperature_hot: float, temperature_cold: float) -> float:
    """
    Calculate the efficiency of a Carnot engine given the temperatures of the hot and cold reservoirs.

    Parameters
    ----------
        temperature_hot (float): The absolute temperature of the hot reservoir (in kelvin).
        temperature_cold (float): The absolute temperature of the cold reservoir (in kelvin).

    Returns
    -------
        float: The efficiency of the Carnot engine (as a decimal).
    """
    if temperature_hot <= 0 or temperature_cold <= 0:
        raise ValueError("Temperatures must be greater than zero.")

    return 1 - (temperature_cold / temperature_hot)


def clausius_clapeyron(
    temperature: float,
    latent_heat: float,
    specific_volume_liquid: float,
    specific_volume_vapor: float,
) -> float:
    """
    Calculate the slope of the phase boundary using the Clausius-Clapeyron equation.

    Parameters
    ----------
        temperature (float): The absolute temperature at which the phase change occurs (in kelvin).
        latent_heat (float): The latent heat of the phase change (in joules per kilogram).
        specific_volume_liquid (float): The specific volume of the liquid phase (in cubic meters per kilogram).
        specific_volume_vapor (float): The specific volume of the vapor phase (in cubic meters per kilogram).

    Returns
    -------
        float: The slope of the phase boundary (in pascals per kelvin).
    """
    return (latent_heat) / (
        temperature * (specific_volume_vapor - specific_volume_liquid)
    )


def helmholtz_free_energy(
    internal_energy: float, temperature: float, entropy: float
) -> float:
    """
    Calculate the Helmholtz free energy given internal energy, temperature, and entropy.

    Parameters
    ----------
        internal_energy (float): The internal energy of the system (in joules).
        temperature (float): The absolute temperature (in kelvin).
        entropy (float): The entropy of the system (in joules per kelvin).

    Returns
    -------
        float: The Helmholtz free energy (in joules).
    """
    return internal_energy - temperature * entropy


def van_der_waals_pressure(
    n: float, vol: float, temp: float, a: float, b: float
) -> Quantity:
    """
    Calculate the pressure of a real gas using the Van der Waals equation.

    Parameters
    ----------
        n (float): The number of moles of the gas.
        vol (float): The volume of the gas (in cubic meters).
        T (float): The absolute temperature of the gas (in kelvin).
        a (float): The Van der Waals constant for attraction (in joules per mole squared).
        b (float): The Van der Waals constant for volume (in cubic meters per mole).

    Returns
    -------
        float: The pressure of the gas (in pascals).
    """
    return Quantity(
        (n * GAS_CONSTANT.value * temp) / (vol - n * b) - (a * n**2) / vol**2, PASCAL
    )
