"""`UniChem` source — chemical formulas, stoichiometry, gases, and solutions.

All molar masses are returned in ``g/mol`` (numerically identical to ``u``),
gas-law pressures/volumes use SI (``Pa``, ``m³``, ``mol``, ``K``), and
concentrations are in ``mol/L`` unless stated otherwise.
"""

from __future__ import annotations

import math
import re as regex
from functools import reduce

from ..uniphys.thermodynamics import ideal_gas_law as _ideal_gas_law
from .elements import ELEMENTS_BY_SYMBOL, atomic_mass
from .exceptions import (
    ChemistryError,
    FormulaError,
    ReactionError,
    SolutionError,
    UnknownElementError,
)

# Separators used for hydrates, e.g. CuSO4·5H2O.
_HYDRATE_SEPARATORS = regex.compile(r"[·⋅*.．]")
_TRAILING_STATE = regex.compile(r"\((?:aq|s|l|g)\)$", regex.IGNORECASE)
_LEADING_COEFFICIENT = regex.compile(r"^\d+")

# Valid equation separator arrows
_VALID_ARROWS = {"->", "→", "=>", "="}

# --------------------------------------------------------------------------- #
# Formula parsing
# --------------------------------------------------------------------------- #


def _read_number(formula: str, idx: int) -> tuple[int, int]:
    """Read an optional integer at ``index``; defaults to 1 when absent."""
    end = idx
    while end < len(formula) and formula[end].isdigit():
        end += 1
    if end == idx:
        return 1, idx
    value = int(formula[idx:end])
    if value == 0:
        raise FormulaError("Stoichiometric subscripts must be positive")
    return value, end


def _parse_part(part: str) -> dict[str, int]:
    """Parse a single (hydrate-free) formula fragment into element counts."""
    counts: dict[str, int] = {}
    stack: list[dict[str, int]] = [counts]
    idx = 0
    length = len(part)

    while idx < length:
        char = part[idx]

        if char in "([":
            stack.append({})
            idx += 1

        elif char in ")]":
            if len(stack) == 1:
                raise FormulaError(f"Unbalanced bracket in formula {part!r}")
            group = stack.pop()
            idx += 1
            multiplier, idx = _read_number(part, idx)
            parent = stack[-1]
            for sym, count in group.items():
                parent[sym] = parent.get(sym, 0) + count * multiplier

        elif char.isupper():
            end = idx + 1
            while end < length and part[end].islower():
                end += 1
            symbol = part[idx:end]
            if symbol not in ELEMENTS_BY_SYMBOL:
                raise UnknownElementError(
                    f"Unknown element symbol {symbol!r} in {part!r}"
                )
            idx = end
            multiplier, idx = _read_number(part, idx)
            stack[-1][symbol] = stack[-1].get(symbol, 0) + multiplier

        else:
            raise FormulaError(f"Unexpected character {char!r} in formula {part!r}")

    if len(stack) != 1:
        raise FormulaError(f"Unbalanced brackets in formula {part!r}")
    if not counts:
        raise FormulaError(f"Formula {part!r} contains no elements")
    return counts


def parse_formula(formula: str) -> dict[str, int]:
    """Parse a chemical formula into a ``{element_symbol: count}`` mapping.

    Supports nested parentheses, hydrates (``·``, ``*``, or ``.``), leading
    coefficients, and charges are ignored (they are not tracked).

    Examples
    --------
    >>> parse_formula("Ca(OH)2")
    {'Ca': 1, 'O': 2, 'H': 2}
    >>> parse_formula("CuSO4·5H2O")
    {'Cu': 1, 'S': 1, 'O': 9, 'H': 10}
    """

    if not isinstance(formula, str):
        raise FormulaError("Formula must be a string")

    cleaned = formula.replace(" ", "")

    if not cleaned:
        raise FormulaError("Formula cannot be empty")

    total: dict[str, int] = {}

    for fragment in _HYDRATE_SEPARATORS.split(cleaned):
        if not fragment:
            raise FormulaError(f"Malformed hydrate in formula {formula!r}")
        coeff, idx = _read_number(fragment, 0)
        remainder = fragment[idx:]
        if not remainder:
            raise FormulaError(f"Malformed hydrate in formula {formula!r}")
        for sym, count in _parse_part(remainder).items():
            total[sym] = total.get(sym, 0) + count * coeff
    return total


def molar_mass(formula: str) -> float:
    """Return the molar mass of a formula in ``g/mol``.

    >>> round(molar_mass("H2O"), 3)
    18.015
    """
    counts = parse_formula(formula)
    return math.fsum(atomic_mass(sym) * count for sym, count in counts.items())


def mass_percent_composition(formula: str) -> dict[str, float]:
    """Return the mass percentage each element contributes to a formula."""
    counts = parse_formula(formula)
    total = molar_mass(formula)
    return {
        sym: (atomic_mass(sym) * count) / total * 100.0 for sym, count in counts.items()
    }


def moles(mass: float, formula: str) -> float:
    """Convert a mass (grams) of a compound to moles."""
    if mass < 0:
        raise ChemistryError("Mass cannot be negative")
    return mass / molar_mass(formula)


def mass(moles: float, formula: str) -> float:
    """Convert an amount in moles of a compound to a mass in grams."""
    if moles < 0:
        raise ChemistryError("Amount of substance cannot be negative")
    return moles * molar_mass(formula)


def empirical_formula(amounts: dict[str, float]) -> str:
    """Return the simplest whole-number formula from element amounts.

    ``amounts`` maps element symbols to relative amounts (moles or mass). The
    ratios are normalized, then scaled to the nearest small integers within a
    1% tolerance.
    """
    if not amounts:
        raise FormulaError("At least one element amount is required")

    for sym in amounts.keys():  # noqa: PLC0206 SIM118
        if sym not in ELEMENTS_BY_SYMBOL:
            raise UnknownElementError(f"Unknown element symbol {sym!r}")
        if amounts[sym] < 0:
            raise FormulaError("Element amounts cannot be negative")

    smallest = min(amounts.values())
    if smallest <= 0:
        raise FormulaError("Element amounts must be strictly positive")

    ratios = {sym: value / smallest for sym, value in amounts.items()}

    # Try scaling factors from 1 upward until all ratios are near-integers.
    for factor in range(1, 101):
        scaled = {sym: ratio * factor for sym, ratio in ratios.items()}
        rounded = {sym: round(value) for sym, value in scaled.items()}
        if all(value >= 1 for value in rounded.values()) and all(
            abs(scaled[sym] - rounded[sym]) <= 0.01 * max(1.0, rounded[sym])
            for sym in scaled
        ):
            return _format_formula(rounded)
    raise FormulaError(f"Could not reduce amounts to an integer formula: {amounts}")


def _format_formula(counts: dict[str, int]) -> str:
    """Render an element-count mapping in Hill order as a formula string."""
    if "C" in counts:
        order = ["C"] + (["H"] if "H" in counts else [])
        order += sorted(sym for sym in counts if sym not in ("C", "H"))
    else:
        order = sorted(counts)
    return "".join(f"{sym}{counts[sym] if counts[sym] != 1 else ''}" for sym in order)


# --------------------------------------------------------------------------- #
# Reactions and stoichiometry
# --------------------------------------------------------------------------- #


def _split_equation(equation: str) -> tuple[list[str], list[str]]:
    """Split an equation string into reactant and product species lists."""

    for arrow in _VALID_ARROWS:
        if arrow in equation:
            l, _, r = equation.partition(arrow)
            break

    else:
        raise ReactionError(
            f"Equation {equation!r} must contain an arrow ('->' or '→')"
        )

    def species(side: str) -> list[str]:
        terms = []
        for term in side.split("+"):
            term = term.replace(" ", "")
            if term:
                terms.append(term)
        return terms

    reactants, products = species(l), species(r)
    if not reactants or not products:
        raise ReactionError(f"Equation {equation!r} is missing reactants or products")
    return reactants, products


def balance_equation(equation: str) -> str:
    """Balance a chemical equation and return it with integer coefficients.

    Any coefficients already present in the input are ignored. State labels
    such as ``(aq)`` and ``(g)`` are preserved.

    >>> balance_equation("H2 + O2 -> H2O")
    '2 H2 + O2 -> 2 H2O'
    """
    import sympy

    reactants, products = _split_equation(equation)

    def as_formula(term: str) -> dict[str, int]:
        return parse_formula(
            _LEADING_COEFFICIENT.sub("", _TRAILING_STATE.sub("", term))
        )

    parsed_reactants = [as_formula(s) for s in reactants]
    parsed_products = [as_formula(s) for s in products]

    elements = sorted(
        {sym for counts in parsed_reactants + parsed_products for sym in counts}
    )

    matrix: list[list[int]] = []

    for sym in elements:
        row = [counts.get(sym, 0) for counts in parsed_reactants]
        row += [-counts.get(sym, 0) for counts in parsed_products]
        matrix.append(row)

    if not any(any(cell != 0 for cell in row) for row in matrix):
        raise ReactionError("Equation contains no elements")

    null_space = sympy.Matrix(matrix).nullspace()

    if not null_space:
        raise ReactionError(f"Equation {equation!r} cannot be balanced")

    vec = null_space[0]
    denominators = [int(sympy.denom(entry)) for entry in vec]

    multiplier = math.lcm(*denominators) if denominators else 1
    ints = [int(entry * multiplier) for entry in vec]

    div = reduce(math.gcd, (abs(val) for val in ints), 0)
    ints = [val // div for val in ints]

    if all(value <= 0 for value in ints):
        ints = [-value for value in ints]

    if any(value <= 0 for value in ints):
        raise ReactionError(f"Equation {equation!r} has no positive integer balance")

    n_reactants = len(reactants)

    def render(specie: str, coeff: int) -> str:
        return specie if coeff == 1 else f"{coeff} {specie}"

    left = " + ".join(
        render(specie, coeff) for specie, coeff in zip(reactants, ints[:n_reactants])
    )
    right = " + ".join(
        render(specie, coeff) for specie, coeff in zip(products, ints[n_reactants:])
    )
    return f"{left} -> {right}"


def percent_yield(actual: float, theoretical: float) -> float:
    """Return the percent yield of a reaction."""
    if theoretical <= 0:
        raise ChemistryError("Theoretical yield must be positive")
    return actual / theoretical * 100.0


# --------------------------------------------------------------------------- #
# Gases
# --------------------------------------------------------------------------- #


def ideal_gas_law(
    *,
    P: float | None = None,
    V: float | None = None,
    n: float | None = None,
    T: float | None = None,
) -> tuple[float, float, float, float]:
    """Solve the ideal gas law ``P·V = n·R·T`` for the single missing term.

    Exactly three of the four keyword arguments must be provided. Returns the
    complete ``(P, V, n, T)`` tuple in SI units (``Pa``, ``m³``, ``mol``, ``K``).
    """
    vals = {"P": P, "V": V, "n": n, "T": T}
    missing = [key for key, value in vals.items() if value is None]
    if len(missing) != 1:
        raise ChemistryError(
            "Provide exactly three of P, V, n, T; missing: "
            + (", ".join(missing) or "none")
        )

    target = missing[0]
    for k, v in vals.items():
        if k != target and v is not None and v <= 0:
            raise ChemistryError(f"{k} must be positive when solving for {target}")

    return _ideal_gas_law(P=P, V=V, n=n, T=T)


# --------------------------------------------------------------------------- #
# Solutions and acid/base chemistry
# --------------------------------------------------------------------------- #


def molarity(moles: float, volume_liters: float) -> float:
    """Return concentration in ``mol/L`` from an amount of solute and volume."""
    if volume_liters <= 0:
        raise SolutionError("Volume must be positive")
    if moles < 0:
        raise SolutionError("Amount of solute cannot be negative")
    return moles / volume_liters


def moles_from_molarity(conc: float, volume_liters: float) -> float:
    """Return the amount of solute (mol) in a solution."""
    if conc < 0 or volume_liters < 0:
        raise SolutionError("Concentration and volume cannot be negative")
    return conc * volume_liters


def dilution(
    *,
    c1: float | None = None,
    v1: float | None = None,
    c2: float | None = None,
    v2: float | None = None,
) -> tuple[float, float, float, float]:
    """Solve ``c1·v1 = c2·v2`` for the single missing quantity.

    Returns the complete ``(c1, v1, c2, v2)`` tuple.
    """
    vals = {"c1": c1, "v1": v1, "c2": c2, "v2": v2}
    missing = [key for key, value in vals.items() if value is None]
    if len(missing) != 1:
        raise SolutionError(
            "Provide exactly three of c1, v1, c2, v2; missing: "
            + (", ".join(missing) or "none")
        )

    for k, v in vals.items():
        if k != missing[0] and v is not None and v < 0:
            raise SolutionError(f"{k} cannot be negative")

    # These assert-statements are only used to satisfy BPR since
    # only one variable can possibly be missing at the same time.
    if missing[0] == "c1":
        assert c2 and v2 and v1
        c1 = c2 * v2 / v1
    elif missing[0] == "v1":
        assert c2 and v2 and c1
        v1 = c2 * v2 / c1
    elif missing[0] == "c2":
        assert c1 and v1 and v2
        c2 = c1 * v1 / v2
    else:
        assert c1 and v1 and c2
        v2 = c1 * v1 / c2
    return (c1, v1, c2, v2)


def ph(conc: float) -> float:
    """Return the pH of a strong-acid solution from its H⁺ concentration."""
    if conc <= 0:
        raise SolutionError("Concentration must be positive for pH")
    return -math.log10(conc)


def poh(conc: float) -> float:
    """Return the pOH of a strong-base solution from its OH⁻ concentration."""
    if conc <= 0:
        raise SolutionError("Concentration must be positive for pOH")
    return -math.log10(conc)


def ph_from_poh(poh: float) -> float:
    """Convert pOH to pH at 25 °C (``pH + pOH = 14``)."""
    return 14.0 - poh


def poh_from_ph(ph: float) -> float:
    """Convert pH to pOH at 25 °C (``pH + pOH = 14``)."""
    return 14.0 - ph


def concentration_from_ph(ph: float) -> float:
    """Return the H⁺ concentration from a pH value."""
    return 10.0 ** (-ph)


def concentration_from_poh(poh: float) -> float:
    """Return the OH⁻ concentration from a pOH value."""
    return 10.0 ** (-poh)


def henderson_hasselbalch(pka: float, base_conc: float, acid_conc: float) -> float:
    """Return the pH of a buffer using the Henderson–Hasselbalch equation."""
    if base_conc <= 0 or acid_conc <= 0:
        raise SolutionError("Buffer concentrations must be positive")
    return pka + math.log10(base_conc / acid_conc)


__all__ = [
    "balance_equation",
    "concentration_from_ph",
    "concentration_from_poh",
    "dilution",
    "empirical_formula",
    "henderson_hasselbalch",
    "ideal_gas_law",
    "mass",
    "mass_percent_composition",
    "molar_mass",
    "molarity",
    "moles",
    "moles_from_molarity",
    "parse_formula",
    "percent_yield",
    "ph",
    "ph_from_poh",
    "poh",
    "poh_from_ph",
]
