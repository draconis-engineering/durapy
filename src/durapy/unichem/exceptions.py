"""Exceptions for the `UniChem` module."""


class ChemistryError(ValueError):
    """Base class for all `UniChem` errors."""


class UnknownElementError(ChemistryError):
    """Raised when an element symbol, name, or atomic number cannot be resolved."""


class FormulaError(ChemistryError):
    """Raised when a chemical formula cannot be parsed."""


class ReactionError(ChemistryError):
    """Raised when a chemical equation cannot be balanced or is invalid."""


class SolutionError(ChemistryError):
    """Raised for invalid concentrations, volumes, or acid/base inputs."""
