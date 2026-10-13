"""Fuse model for the `UniPower` module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fuse:
    """A current-limiting fuse.

    Parameters
    ----------
    rating_current:
        Rated (hold) current in amperes. The fuse is considered blown when the
        current exceeds this value.
    voltage_rating:
        Maximum voltage in volts. Optional.
    """

    rating_current: float
    voltage_rating: float | None = None

    def __post_init__(self) -> None:
        if self.rating_current <= 0:
            raise ValueError("rating_current must be positive")
        if self.voltage_rating is not None and self.voltage_rating <= 0:
            raise ValueError("voltage_rating must be positive")

    def is_within_rating(self, current: float) -> bool:
        """Whether ``current`` is at or below the rating (fuse holds)."""
        return abs(current) <= self.rating_current

    def will_blow(self, current: float) -> bool:
        """Whether ``current`` exceeds the rating and would blow the fuse."""
        return abs(current) > self.rating_current

    def percent_loaded(self, current: float) -> float:
        """Load as a percentage of the rated current."""
        return 100 * abs(current) / self.rating_current
