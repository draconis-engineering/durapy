"""`UniChem` periodic table data and element lookups.

The :data:`ELEMENTS` table stores standard atomic weights (IUPAC conventional
values). For elements with no stable isotopes, the mass number of the most
stable known isotope is used and is therefore an integer.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from types import MappingProxyType

from .exceptions import UnknownElementError

# Categories used throughout the periodic table.
ALKALI = "alkali metal"
ALKALINE_EARTH = "alkaline earth metal"
TRANSITION = "transition metal"
POST_TRANSITION = "post-transition metal"
METALLOID = "metalloid"
NONMETAL = "reactive nonmetal"
HALOGEN = "halogen"
NOBLE_GAS = "noble gas"
LANTHANIDE = "lanthanide"
ACTINIDE = "actinide"

# Switch to set here?
CATEGORIES = (
    ALKALI,
    ALKALINE_EARTH,
    TRANSITION,
    POST_TRANSITION,
    METALLOID,
    NONMETAL,
    HALOGEN,
    NOBLE_GAS,
    LANTHANIDE,
    ACTINIDE,
)


@dataclass(frozen=True, slots=True)
class Element:
    """A single chemical element."""

    atomic_number: int
    symbol: str
    name: str
    atomic_mass: float
    category: str
    group: int | None
    period: int

    @property
    def mass_number(self) -> int:
        """The mass number (nearest integer to the atomic mass)."""
        return round(self.atomic_mass)

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return (
            f"Element({self.atomic_number}, {self.symbol!r}, {self.name!r}, "
            f"{self.atomic_mass!r}, {self.category!r}, {self.group!r}, {self.period!r})"
        )


# (Z, symbol, name, atomic_mass, category, group, period)
_DATA: tuple[tuple[int, str, str, float, str, int | None, int], ...] = (
    (1, "H", "Hydrogen", 1.008, NONMETAL, 1, 1),
    (2, "He", "Helium", 4.002602, NOBLE_GAS, 18, 1),
    (3, "Li", "Lithium", 6.94, ALKALI, 1, 2),
    (4, "Be", "Beryllium", 9.0121831, ALKALINE_EARTH, 2, 2),
    (5, "B", "Boron", 10.81, METALLOID, 13, 2),
    (6, "C", "Carbon", 12.011, NONMETAL, 14, 2),
    (7, "N", "Nitrogen", 14.007, NONMETAL, 15, 2),
    (8, "O", "Oxygen", 15.999, NONMETAL, 16, 2),
    (9, "F", "Fluorine", 18.998403163, HALOGEN, 17, 2),
    (10, "Ne", "Neon", 20.1797, NOBLE_GAS, 18, 2),
    (11, "Na", "Sodium", 22.98976928, ALKALI, 1, 3),
    (12, "Mg", "Magnesium", 24.305, ALKALINE_EARTH, 2, 3),
    (13, "Al", "Aluminium", 26.9815385, POST_TRANSITION, 13, 3),
    (14, "Si", "Silicon", 28.085, METALLOID, 14, 3),
    (15, "P", "Phosphorus", 30.973761998, NONMETAL, 15, 3),
    (16, "S", "Sulfur", 32.06, NONMETAL, 16, 3),
    (17, "Cl", "Chlorine", 35.45, HALOGEN, 17, 3),
    (18, "Ar", "Argon", 39.948, NOBLE_GAS, 18, 3),
    (19, "K", "Potassium", 39.0983, ALKALI, 1, 4),
    (20, "Ca", "Calcium", 40.078, ALKALINE_EARTH, 2, 4),
    (21, "Sc", "Scandium", 44.955908, TRANSITION, 3, 4),
    (22, "Ti", "Titanium", 47.867, TRANSITION, 4, 4),
    (23, "V", "Vanadium", 50.9415, TRANSITION, 5, 4),
    (24, "Cr", "Chromium", 51.9961, TRANSITION, 6, 4),
    (25, "Mn", "Manganese", 54.938044, TRANSITION, 7, 4),
    (26, "Fe", "Iron", 55.845, TRANSITION, 8, 4),
    (27, "Co", "Cobalt", 58.933194, TRANSITION, 9, 4),
    (28, "Ni", "Nickel", 58.6934, TRANSITION, 10, 4),
    (29, "Cu", "Copper", 63.546, TRANSITION, 11, 4),
    (30, "Zn", "Zinc", 65.38, TRANSITION, 12, 4),
    (31, "Ga", "Gallium", 69.723, POST_TRANSITION, 13, 4),
    (32, "Ge", "Germanium", 72.63, METALLOID, 14, 4),
    (33, "As", "Arsenic", 74.921595, METALLOID, 15, 4),
    (34, "Se", "Selenium", 78.971, NONMETAL, 16, 4),
    (35, "Br", "Bromine", 79.904, HALOGEN, 17, 4),
    (36, "Kr", "Krypton", 83.798, NOBLE_GAS, 18, 4),
    (37, "Rb", "Rubidium", 85.4678, ALKALI, 1, 5),
    (38, "Sr", "Strontium", 87.62, ALKALINE_EARTH, 2, 5),
    (39, "Y", "Yttrium", 88.90584, TRANSITION, 3, 5),
    (40, "Zr", "Zirconium", 91.224, TRANSITION, 4, 5),
    (41, "Nb", "Niobium", 92.90637, TRANSITION, 5, 5),
    (42, "Mo", "Molybdenum", 95.95, TRANSITION, 6, 5),
    (43, "Tc", "Technetium", 98.0, TRANSITION, 7, 5),
    (44, "Ru", "Ruthenium", 101.07, TRANSITION, 8, 5),
    (45, "Rh", "Rhodium", 102.9055, TRANSITION, 9, 5),
    (46, "Pd", "Palladium", 106.42, TRANSITION, 10, 5),
    (47, "Ag", "Silver", 107.8682, TRANSITION, 11, 5),
    (48, "Cd", "Cadmium", 112.414, TRANSITION, 12, 5),
    (49, "In", "Indium", 114.818, POST_TRANSITION, 13, 5),
    (50, "Sn", "Tin", 118.71, POST_TRANSITION, 14, 5),
    (51, "Sb", "Antimony", 121.76, METALLOID, 15, 5),
    (52, "Te", "Tellurium", 127.6, METALLOID, 16, 5),
    (53, "I", "Iodine", 126.90447, HALOGEN, 17, 5),
    (54, "Xe", "Xenon", 131.293, NOBLE_GAS, 18, 5),
    (55, "Cs", "Caesium", 132.90545196, ALKALI, 1, 6),
    (56, "Ba", "Barium", 137.327, ALKALINE_EARTH, 2, 6),
    (57, "La", "Lanthanum", 138.90547, LANTHANIDE, 3, 6),
    (58, "Ce", "Cerium", 140.116, LANTHANIDE, None, 6),
    (59, "Pr", "Praseodymium", 140.90766, LANTHANIDE, None, 6),
    (60, "Nd", "Neodymium", 144.242, LANTHANIDE, None, 6),
    (61, "Pm", "Promethium", 145.0, LANTHANIDE, None, 6),
    (62, "Sm", "Samarium", 150.36, LANTHANIDE, None, 6),
    (63, "Eu", "Europium", 151.964, LANTHANIDE, None, 6),
    (64, "Gd", "Gadolinium", 157.25, LANTHANIDE, None, 6),
    (65, "Tb", "Terbium", 158.92535, LANTHANIDE, None, 6),
    (66, "Dy", "Dysprosium", 162.5, LANTHANIDE, None, 6),
    (67, "Ho", "Holmium", 164.93033, LANTHANIDE, None, 6),
    (68, "Er", "Erbium", 167.259, LANTHANIDE, None, 6),
    (69, "Tm", "Thulium", 168.93422, LANTHANIDE, None, 6),
    (70, "Yb", "Ytterbium", 173.045, LANTHANIDE, None, 6),
    (71, "Lu", "Lutetium", 174.9668, LANTHANIDE, None, 6),
    (72, "Hf", "Hafnium", 178.49, TRANSITION, 4, 6),
    (73, "Ta", "Tantalum", 180.94788, TRANSITION, 5, 6),
    (74, "W", "Tungsten", 183.84, TRANSITION, 6, 6),
    (75, "Re", "Rhenium", 186.207, TRANSITION, 7, 6),
    (76, "Os", "Osmium", 190.23, TRANSITION, 8, 6),
    (77, "Ir", "Iridium", 192.217, TRANSITION, 9, 6),
    (78, "Pt", "Platinum", 195.084, TRANSITION, 10, 6),
    (79, "Au", "Gold", 196.966569, TRANSITION, 11, 6),
    (80, "Hg", "Mercury", 200.592, TRANSITION, 12, 6),
    (81, "Tl", "Thallium", 204.38, POST_TRANSITION, 13, 6),
    (82, "Pb", "Lead", 207.2, POST_TRANSITION, 14, 6),
    (83, "Bi", "Bismuth", 208.9804, POST_TRANSITION, 15, 6),
    (84, "Po", "Polonium", 209.0, POST_TRANSITION, 16, 6),
    (85, "At", "Astatine", 210.0, HALOGEN, 17, 6),
    (86, "Rn", "Radon", 222.0, NOBLE_GAS, 18, 6),
    (87, "Fr", "Francium", 223.0, ALKALI, 1, 7),
    (88, "Ra", "Radium", 226.0, ALKALINE_EARTH, 2, 7),
    (89, "Ac", "Actinium", 227.0, ACTINIDE, 3, 7),
    (90, "Th", "Thorium", 232.0377, ACTINIDE, None, 7),
    (91, "Pa", "Protactinium", 231.03588, ACTINIDE, None, 7),
    (92, "U", "Uranium", 238.02891, ACTINIDE, None, 7),
    (93, "Np", "Neptunium", 237.0, ACTINIDE, None, 7),
    (94, "Pu", "Plutonium", 244.0, ACTINIDE, None, 7),
    (95, "Am", "Americium", 243.0, ACTINIDE, None, 7),
    (96, "Cm", "Curium", 247.0, ACTINIDE, None, 7),
    (97, "Bk", "Berkelium", 247.0, ACTINIDE, None, 7),
    (98, "Cf", "Californium", 251.0, ACTINIDE, None, 7),
    (99, "Es", "Einsteinium", 252.0, ACTINIDE, None, 7),
    (100, "Fm", "Fermium", 257.0, ACTINIDE, None, 7),
    (101, "Md", "Mendelevium", 258.0, ACTINIDE, None, 7),
    (102, "No", "Nobelium", 259.0, ACTINIDE, None, 7),
    (103, "Lr", "Lawrencium", 266.0, ACTINIDE, None, 7),
    (104, "Rf", "Rutherfordium", 267.0, TRANSITION, 4, 7),
    (105, "Db", "Dubnium", 268.0, TRANSITION, 5, 7),
    (106, "Sg", "Seaborgium", 269.0, TRANSITION, 6, 7),
    (107, "Bh", "Bohrium", 270.0, TRANSITION, 7, 7),
    (108, "Hs", "Hassium", 269.0, TRANSITION, 8, 7),
    (109, "Mt", "Meitnerium", 278.0, TRANSITION, 9, 7),
    (110, "Ds", "Darmstadtium", 281.0, TRANSITION, 10, 7),
    (111, "Rg", "Roentgenium", 282.0, TRANSITION, 11, 7),
    (112, "Cn", "Copernicium", 285.0, TRANSITION, 12, 7),
    (113, "Nh", "Nihonium", 286.0, POST_TRANSITION, 13, 7),
    (114, "Fl", "Flerovium", 289.0, POST_TRANSITION, 14, 7),
    (115, "Mc", "Moscovium", 290.0, POST_TRANSITION, 15, 7),
    (116, "Lv", "Livermorium", 293.0, POST_TRANSITION, 16, 7),
    (117, "Ts", "Tennessine", 294.0, HALOGEN, 17, 7),
    (118, "Og", "Oganesson", 294.0, NOBLE_GAS, 18, 7),
)

ELEMENTS: tuple[Element, ...] = tuple(
    Element(z, sym, name, mass, cat, group, period)
    for z, sym, name, mass, cat, group, period in _DATA
)

ELEMENTS_BY_SYMBOL: MappingProxyType[str, Element] = MappingProxyType(
    {element.symbol: element for element in ELEMENTS}
)
ELEMENTS_BY_NAME: MappingProxyType[str, Element] = MappingProxyType(
    {element.name.lower(): element for element in ELEMENTS}
)
ELEMENTS_BY_NUMBER: MappingProxyType[int, Element] = MappingProxyType(
    {element.atomic_number: element for element in ELEMENTS}
)


def element(query: int | str) -> Element:
    """Look up an element by atomic number, symbol, or full name.

    Lookups are case-insensitive for symbols and names: ``element("na")``,
    ``element("Na")``, ``element("sodium")`` and ``element(11)`` all return the
    same :class:`Element`.

    Raises
    ------
    UnknownElementError
        If no element matches ``query``.
    """
    if isinstance(query, bool):  # bool is a subclass of int; reject it explicitly
        raise UnknownElementError("Element query must be an int or str, not bool")
    if isinstance(query, int):
        try:
            return ELEMENTS_BY_NUMBER[query]
        except KeyError:
            raise UnknownElementError(
                f"No element with atomic number {query}"
            ) from None
    if isinstance(query, str):
        cleaned = query.strip()
        if not cleaned:
            raise UnknownElementError("Element query cannot be empty")
        by_symbol = ELEMENTS_BY_SYMBOL.get(cleaned.capitalize())
        if by_symbol is not None:
            return by_symbol
        by_name = ELEMENTS_BY_NAME.get(cleaned.lower())
        if by_name is not None:
            return by_name
        if cleaned.isdigit():
            return element(int(cleaned))
        raise UnknownElementError(f"Unknown element: {query!r}")
    raise UnknownElementError(
        f"Element query must be an int or str, got {type(query).__name__}"
    )


def atomic_mass(query: int | str) -> float:
    """Return the standard atomic mass (in u / g·mol⁻¹) of an element."""
    return element(query).atomic_mass


def atomic_number(query: str | int) -> int:
    """Return the atomic number of an element by name or symbol."""
    return element(query).atomic_number


def symbol(query: int | str) -> str:
    """Return the element symbol for a given name, symbol, or atomic number."""
    return element(query).symbol


def name(query: int | str) -> str:
    """Return the full element name for a given name, symbol, or atomic number."""
    return element(query).name


def elements_by_category(category: str) -> list[Element]:
    """Return all elements belonging to ``category`` (see :data:`CATEGORIES`)."""
    wanted = category.strip().lower()
    if wanted not in CATEGORIES:
        raise UnknownElementError(
            f"Unknown category {category!r}. Valid categories: {', '.join(CATEGORIES)}"
        )
    return [element for element in ELEMENTS if element.category == wanted]


def elements_by_period(period: int) -> list[Element]:
    """Return all elements in the given period (row)."""
    return [element for element in ELEMENTS if element.period == period]


def elements_by_group(group: int) -> list[Element]:
    """Return all elements in the given group (column)."""
    return [element for element in ELEMENTS if element.group == group]


def iter_elements() -> Iterator[Element]:
    """Iterate over every element in ascending atomic-number order."""
    return iter(ELEMENTS)
