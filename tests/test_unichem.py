"""Tests for the `durapy.unichem` module."""

import math

import pytest

from durapy import unichem

# --------------------------------------------------------------------------- #
# Elements
# --------------------------------------------------------------------------- #


def test_element_lookup_by_number_symbol_and_name():
    assert unichem.element(11).symbol == "Na"
    assert unichem.element("na").atomic_number == 11
    assert unichem.element("Sodium").name == "Sodium"
    assert unichem.atomic_mass("H") == pytest.approx(1.008)
    assert unichem.atomic_number("O") == 8
    assert unichem.symbol(6) == "C"
    assert unichem.name("fe") == "Iron"


def test_element_table_is_complete_and_reversible():
    assert len(unichem.ELEMENTS) == 118
    assert [element.atomic_number for element in unichem.ELEMENTS] == list(
        range(1, 119)
    )
    for element in unichem.ELEMENTS:
        assert unichem.ELEMENTS_BY_SYMBOL[element.symbol] is element
        assert unichem.ELEMENTS_BY_NUMBER[element.atomic_number] is element


def test_element_queries_reject_bad_input():
    with pytest.raises(unichem.UnknownElementError):
        unichem.element(999)
    with pytest.raises(unichem.UnknownElementError):
        unichem.element("Unobtainium")
    with pytest.raises(unichem.UnknownElementError):
        unichem.element("")
    with pytest.raises(unichem.UnknownElementError):
        unichem.element(True)  # bool must not be treated as atomic number 1


def test_element_grouping():
    noble_gases = [element.symbol for element in unichem.elements_by_group(18)]
    assert noble_gases[0] == "He" and noble_gases[-1] == "Og"
    assert len(unichem.elements_by_period(1)) == 2
    assert "Fe" in [
        element.symbol for element in unichem.elements_by_category(unichem.TRANSITION)
    ]
    with pytest.raises(unichem.UnknownElementError):
        unichem.elements_by_category("plasma")


# --------------------------------------------------------------------------- #
# Formula parsing and molar mass
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("formula", "expected"),
    [
        ("H2O", {"H": 2, "O": 1}),
        ("H2SO4", {"H": 2, "S": 1, "O": 4}),
        ("Ca(OH)2", {"Ca": 1, "O": 2, "H": 2}),
        ("Al2(SO4)3", {"Al": 2, "S": 3, "O": 12}),
        ("C6H12O6", {"C": 6, "H": 12, "O": 6}),
        ("CuSO4·5H2O", {"Cu": 1, "S": 1, "O": 9, "H": 10}),
        ("2H2O", {"H": 4, "O": 2}),
    ],
)
def test_parse_formula(formula, expected):
    assert unichem.parse_formula(formula) == expected


def test_parse_formula_errors():
    with pytest.raises(unichem.UnknownElementError):
        unichem.parse_formula("Xx2")
    with pytest.raises(unichem.FormulaError):
        unichem.parse_formula("H2O)")
    with pytest.raises(unichem.FormulaError):
        unichem.parse_formula("")
    with pytest.raises(unichem.FormulaError):
        unichem.parse_formula("H2O$")


@pytest.mark.parametrize(
    ("formula", "expected"),
    [
        ("H2O", 18.015),
        ("C6H12O6", 180.156),
        ("Ca(OH)2", 74.093),
        ("NaCl", 58.44),
    ],
)
def test_molar_mass(formula, expected):
    assert unichem.molar_mass(formula) == pytest.approx(expected, abs=0.01)


def test_mass_percent_composition():
    composition = unichem.mass_percent_composition("H2O")
    assert sum(composition.values()) == pytest.approx(100.0)
    assert composition["O"] == pytest.approx(88.81, abs=0.05)


def test_moles_and_mass_round_trip():
    assert unichem.moles(18.015, "H2O") == pytest.approx(1.0, abs=1e-3)
    assert unichem.mass(1.0, "H2O") == pytest.approx(18.015, abs=1e-3)
    with pytest.raises(unichem.ChemistryError):
        unichem.moles(-1, "H2O")


def test_empirical_formula():
    assert unichem.empirical_formula({"C": 6, "H": 12, "O": 6}) == "CH2O"
    assert unichem.empirical_formula({"H": 2, "O": 1}) == "H2O"
    with pytest.raises(unichem.FormulaError):
        unichem.empirical_formula({"C": 0})


# --------------------------------------------------------------------------- #
# Reactions
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "equation",
    [
        "H2 + O2 -> H2O",
        "CH4 + O2 -> CO2 + H2O",
        "Fe + O2 -> Fe2O3",
        "C2H6 + O2 -> CO2 + H2O",
        "KClO3 -> KCl + O2",
    ],
)
def test_balance_equation_is_conserved(equation):
    balanced = unichem.balance_equation(equation)
    left, _, right = balanced.partition("->")

    def tally(side):
        totals = {}
        for term in side.split("+"):
            term = term.strip()
            coeff = ""
            while term and term[0].isdigit():
                coeff += term[0]
                term = term[1:]
            counts = unichem.parse_formula(term)
            for sym, count in counts.items():
                totals[sym] = totals.get(sym, 0) + count * (int(coeff) if coeff else 1)
        return totals

    assert tally(left) == tally(right)


def test_balance_equation_specific_results():
    assert unichem.balance_equation("H2 + O2 -> H2O") == "2 H2 + O2 -> 2 H2O"
    assert (
        unichem.balance_equation("CH4 + O2 -> CO2 + H2O") == "CH4 + 2 O2 -> CO2 + 2 H2O"
    )
    assert unichem.balance_equation("Fe + O2 -> Fe2O3") == "4 Fe + 3 O2 -> 2 Fe2O3"


def test_balance_equation_preserves_state_labels():
    assert (
        unichem.balance_equation("HCl(aq) + NaOH(aq) -> NaCl(aq) + H2O(l)")
        == "HCl(aq) + NaOH(aq) -> NaCl(aq) + H2O(l)"
    )


def test_balance_equation_errors():
    with pytest.raises(unichem.ReactionError):
        unichem.balance_equation("H2O")
    with pytest.raises(unichem.ReactionError):
        unichem.balance_equation("->")


def test_percent_yield():
    assert unichem.percent_yield(8.0, 10.0) == pytest.approx(80.0)
    with pytest.raises(unichem.ChemistryError):
        unichem.percent_yield(1.0, 0.0)


# --------------------------------------------------------------------------- #
# Gases
# --------------------------------------------------------------------------- #


def test_ideal_gas_law_solves_each_variable():
    pressure, volume, amount, temperature = unichem.ideal_gas_law(
        P=101325.0, V=0.022414, T=273.15
    )
    assert amount == pytest.approx(1.0, abs=1e-3)

    solved = unichem.ideal_gas_law(V=0.022414, n=1.0, T=273.15)
    assert solved[0] == pytest.approx(101325.0, rel=1e-2)

    assert unichem.ideal_gas_law(P=101325.0, V=0.022414, n=1.0)[3] == pytest.approx(
        273.15, rel=1e-2
    )


def test_ideal_gas_law_requires_three_values():
    with pytest.raises(unichem.ChemistryError):
        unichem.ideal_gas_law(P=101325.0, V=0.022414)
    with pytest.raises(unichem.ChemistryError):
        unichem.ideal_gas_law(P=101325.0, V=0.022414, n=1.0, T=273.15)


# --------------------------------------------------------------------------- #
# Solutions and acid/base
# --------------------------------------------------------------------------- #


def test_molarity_and_dilution():
    assert unichem.molarity(0.5, 1.0) == pytest.approx(0.5)
    assert unichem.moles_from_molarity(0.5, 2.0) == pytest.approx(1.0)

    c1, v1, c2, v2 = unichem.dilution(c1=2.0, c2=0.5, v2=100.0)
    assert v1 == pytest.approx(25.0)
    with pytest.raises(unichem.SolutionError):
        unichem.dilution(c1=2.0, c2=0.5)


def test_ph_and_poh_relationships():
    assert unichem.ph(0.01) == pytest.approx(2.0)
    assert unichem.poh(0.1) == pytest.approx(1.0)
    assert unichem.ph_from_poh(1.0) == pytest.approx(13.0)
    assert unichem.poh_from_ph(2.0) == pytest.approx(12.0)
    assert unichem.concentration_from_ph(3.0) == pytest.approx(1e-3)
    assert unichem.concentration_from_poh(4.0) == pytest.approx(1e-4)
    assert unichem.henderson_hasselbalch(4.76, 0.1, 0.1) == pytest.approx(4.76)
    with pytest.raises(unichem.SolutionError):
        unichem.ph(0.0)
    with pytest.raises(unichem.SolutionError):
        unichem.henderson_hasselbalch(4.76, 0.0, 0.1)


def test_solution_math_is_finite():
    for value in (1e-7, 1e-3, 1.0):
        assert math.isfinite(unichem.ph(value))
