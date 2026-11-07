"""Tests for the UniPhys domain layout."""

import importlib.util
import math

import pytest

from durapy import uniphys
from durapy.uniphys.astrophysics import (
    cosmology,
    gravitation,
    orbital_mechanics,
    rocketry,
)
from durapy.uniphys.classical import (
    acoustics,
    electromagnetism,
    fluids,
    mechanics,
    thermodynamics,
)
from durapy.uniphys.modern import nuclear, relativity


def test_domains_are_exported():
    assert uniphys.__all__ == ["astrophysics", "classical", "modern"]
    assert mechanics.kinetic_energy(2, 10).value == pytest.approx(100)
    assert relativity.einstein_mass_energy_equivalence(1).value == pytest.approx(
        mechanics.einstein_mass_energy_equivalence(1).value
    )


def test_legacy_top_level_modules_are_gone():
    for name in (
        "acoustics",
        "electromagnetics",
        "fluid_dynamics",
        "mechanics",
        "nuclear",
        "thermodynamics",
    ):
        assert importlib.util.find_spec(f"durapy.uniphys.{name}") is None


def test_domain_modules_expose_expected_functions():
    assert thermodynamics.ideal_gas_law(
        V=0.022414, n=1.0, T=273.15
    )[0] == pytest.approx(101324.86, rel=1e-4)
    assert fluids.reynolds_number(2, 0.1, 1.5e-5) == pytest.approx(13333.333)
    assert acoustics.sound_speed(293).value == pytest.approx(343.115, rel=1e-4)
    assert electromagnetism.wavelength(1e9).value == pytest.approx(0.299792458)
    assert nuclear.half_life(math.log(2)).value == pytest.approx(1.0)


def test_astrophysics_subdomains_are_importable():
    assert gravitation.schwarzschild_radius(1).value == pytest.approx(1.485e-27)
    assert orbital_mechanics.orbital_velocity(orbital_radius=1, mass=1).value > 0
    assert cosmology.redshift(λobs=2, λrest=1).value == pytest.approx(1)
    assert rocketry.tsiolkovsky_rocket_equation(
        exhaust_vel=1, initial_mass=2, final_mass=1
    ).value == pytest.approx(math.log(2))
