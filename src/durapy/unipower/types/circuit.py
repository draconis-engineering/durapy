"""A small linear circuit solver for the `UniPower` module.

The :class:`Circuit` class performs modified nodal analysis (MNA) on a network
of linear elements. Node ``ground`` (default ``0``) is the reference node.

* :meth:`Circuit.solve_dc` treats capacitors as open circuits and inductors as
  ideal shorts (0 V sources) — the standard DC treatment.
* :meth:`Circuit.solve_ac` performs sinusoidal steady-state (phasor) analysis
  at a given frequency using complex impedances.

Voltage and current source values may be complex, which allows phased AC
sources to be modelled directly.

Example
-------
>>> from durapy.unipower.types.circuit import Circuit
>>> c = Circuit()
>>> _ = c.add_voltage_source(1, 0, 10.0)
>>> _ = c.add_resistor(1, 2, 1000.0)
>>> r2 = c.add_resistor(2, 0, 1000.0)
>>> sol = c.solve_dc()
>>> round(sol.voltage(2).value, 6)
5.0
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from ...shared.numval_types import Quantity
from ...shared.units import AMPERE, OHM, VOLT
from ..exceptions import CircuitError
from .capacitor import Capacitor
from .inductor import Inductor
from .resistor import Resistor


@dataclass
class Element:
    """A handle to an element placed in a :class:`Circuit`.

    Returned by the ``add_*`` methods so that a solution can be queried for the
    element's current.
    """

    kind: str  # "R", "C", "L", "V" or "I"
    n1: int
    n2: int
    value: complex
    label: str | None = None

    def __repr__(self) -> str:
        return (
            f"Element({self.kind}, n1={self.n1}, n2={self.n2}, "
            f"value={self.value!r}, label={self.label!r})"
        )


@dataclass
class CircuitSolution:
    """The result of a DC or AC circuit solve."""

    frequency: float | None
    node_voltages: dict[int, complex]
    element_currents: dict[int, complex] = field(default_factory=dict)

    def voltage_phasor(self, node: int) -> complex:
        """Complex node voltage (V); the imaginary part is 0 for DC."""
        return self.node_voltages.get(node, 0j)

    def voltage(self, node: int) -> Quantity:
        """Node voltage as a :class:`Quantity` in volts."""
        return Quantity(self.voltage_phasor(node), VOLT)

    def current_phasor(self, element: Element) -> complex:
        """Complex current through ``element`` in amperes.

        The sign follows the element's ``n1 -> n2`` direction.
        """
        try:
            return self.element_currents[id(element)]
        except KeyError as exc:
            raise CircuitError(
                "Element does not belong to the solved circuit"
            ) from exc

    def current(self, element: Element) -> Quantity:
        """Current through ``element`` as a :class:`Quantity` in amperes."""
        return Quantity(self.current_phasor(element), AMPERE)

    def node_voltage_map(self) -> dict[int, Quantity]:
        """All solved node voltages as quantities in volts."""
        return {node: Quantity(v, VOLT) for node, v in self.node_voltages.items()}


class Circuit:
    """A linear circuit that can be solved with modified nodal analysis."""

    def __init__(self, ground: int = 0) -> None:
        if not isinstance(ground, int) or isinstance(ground, bool) or ground < 0:
            raise ValueError("ground must be a non-negative integer")
        self._ground = ground
        self._elements: list[Element] = []

    @property
    def ground(self) -> int:
        """The reference (ground) node index."""
        return self._ground

    @property
    def elements(self) -> tuple[Element, ...]:
        """A tuple of the elements currently placed in the circuit."""
        return tuple(self._elements)

    # ------------------------------------------------------------------ #
    # Construction
    # ------------------------------------------------------------------ #

    @staticmethod
    def _validate_nodes(*nodes: int) -> None:
        for node in nodes:
            if not isinstance(node, int) or isinstance(node, bool) or node < 0:
                raise ValueError("node indices must be non-negative integers")

    def _add(
        self, kind: str, n1: int, n2: int, value: complex, label: str | None
    ) -> Element:
        self._validate_nodes(n1, n2)
        if n1 == n2:
            raise ValueError("an element cannot connect a node to itself")
        element = Element(kind, n1, n2, complex(value), label)
        self._elements.append(element)
        return element

    def add_resistor(
        self, n1: int, n2: int, resistance: float, label: str | None = None
    ) -> Element:
        """Add a resistor of ``resistance`` ohms between ``n1`` and ``n2``."""
        if resistance <= 0:
            raise ValueError("resistance must be positive")
        return self._add("R", n1, n2, resistance, label)

    def add_capacitor(
        self, n1: int, n2: int, capacitance: float, label: str | None = None
    ) -> Element:
        """Add a capacitor of ``capacitance`` farads between ``n1`` and ``n2``."""
        if capacitance <= 0:
            raise ValueError("capacitance must be positive")
        return self._add("C", n1, n2, capacitance, label)

    def add_inductor(
        self, n1: int, n2: int, inductance: float, label: str | None = None
    ) -> Element:
        """Add an inductor of ``inductance`` henrys between ``n1`` and ``n2``."""
        if inductance <= 0:
            raise ValueError("inductance must be positive")
        return self._add("L", n1, n2, inductance, label)

    def add_voltage_source(
        self, n_pos: int, n_neg: int, voltage: complex, label: str | None = None
    ) -> Element:
        """Add an ideal voltage source, ``V(n_pos) - V(n_neg) = voltage``."""
        return self._add("V", n_pos, n_neg, voltage, label)

    def add_current_source(
        self, n_from: int, n_to: int, current: complex, label: str | None = None
    ) -> Element:
        """Add an ideal current source.

        Pushes ``current`` amperes out of ``n_from`` and back into ``n_to``.
        """
        return self._add("I", n_from, n_to, current, label)

    def add_component(
        self,
        component: Resistor | Capacitor | Inductor,
        n1: int,
        n2: int,
        label: str | None = None,
    ) -> Element:
        """Add a resistor, capacitor or inductor model between two nodes."""
        if isinstance(component, Resistor):
            return self.add_resistor(n1, n2, component.ohms.value, label)
        if isinstance(component, Capacitor):
            return self.add_capacitor(n1, n2, component.capacitance, label)
        if isinstance(component, Inductor):
            return self.add_inductor(n1, n2, component.inductance, label)
        raise TypeError(
            f"Cannot add a {type(component).__name__} to a linear circuit"
        )

    # ------------------------------------------------------------------ #
    # Solving
    # ------------------------------------------------------------------ #

    def _node_map(self) -> dict[int, int]:
        nodes: set[int] = set()
        for element in self._elements:
            nodes.add(element.n1)
            nodes.add(element.n2)
        nodes.discard(self._ground)
        return {node: i for i, node in enumerate(sorted(nodes))}

    def _solve(self, omega: float | None) -> CircuitSolution:
        index = self._node_map()
        n = len(index)

        vsources = [
            e
            for e in self._elements
            if e.kind == "V" or (e.kind == "L" and omega is None)
        ]
        vs_slot = {id(e): n + k for k, e in enumerate(vsources)}
        size = n + len(vsources)
        if size == 0:
            raise CircuitError("Circuit has no elements to solve")

        matrix = np.zeros((size, size), dtype=complex)
        rhs = np.zeros(size, dtype=complex)

        def stamp_admittance(a: int, b: int, y: complex) -> None:
            ia, ib = index.get(a), index.get(b)
            if ia is not None:
                matrix[ia, ia] += y
            if ib is not None:
                matrix[ib, ib] += y
            if ia is not None and ib is not None:
                matrix[ia, ib] -= y
                matrix[ib, ia] -= y

        def stamp_voltage_source(element: Element, slot: int, value: complex) -> None:
            ia, ib = index.get(element.n1), index.get(element.n2)
            if ia is not None:
                matrix[ia, slot] += 1
                matrix[slot, ia] += 1
            if ib is not None:
                matrix[ib, slot] -= 1
                matrix[slot, ib] -= 1
            rhs[slot] = value

        for element in self._elements:
            if element.kind == "R":
                stamp_admittance(element.n1, element.n2, 1.0 / element.value)
            elif element.kind == "C":
                if omega is None:
                    continue  # open circuit in DC
                stamp_admittance(element.n1, element.n2, 1j * omega * element.value)
            elif element.kind == "L":
                if omega is None:
                    stamp_voltage_source(element, vs_slot[id(element)], 0j)
                else:
                    stamp_admittance(
                        element.n1, element.n2, 1.0 / (1j * omega * element.value)
                    )
            elif element.kind == "V":
                stamp_voltage_source(element, vs_slot[id(element)], element.value)
            elif element.kind == "I":
                ia, ib = index.get(element.n1), index.get(element.n2)
                if ia is not None:
                    rhs[ia] += element.value
                if ib is not None:
                    rhs[ib] -= element.value

        try:
            solution = np.linalg.solve(matrix, rhs)
        except np.linalg.LinAlgError as exc:
            raise CircuitError(
                "Circuit is singular: check for floating nodes or a missing "
                "ground reference"
            ) from exc

        node_voltages: dict[int, complex] = {self._ground: 0j}
        for node, i in index.items():
            node_voltages[node] = complex(solution[i])

        def node_voltage(node: int) -> complex:
            return node_voltages.get(node, 0j)

        currents: dict[int, complex] = {}
        for element in self._elements:
            drop = node_voltage(element.n1) - node_voltage(element.n2)
            if element.kind == "R":
                currents[id(element)] = drop / element.value
            elif element.kind == "C":
                currents[id(element)] = (
                    0j if omega is None else drop * (1j * omega * element.value)
                )
            elif element.kind == "L":
                currents[id(element)] = (
                    complex(solution[vs_slot[id(element)]])
                    if omega is None
                    else drop / (1j * omega * element.value)
                )
            elif element.kind == "V":
                currents[id(element)] = complex(solution[vs_slot[id(element)]])
            elif element.kind == "I":
                currents[id(element)] = complex(element.value)

        return CircuitSolution(omega, node_voltages, currents)

    def solve_dc(self) -> CircuitSolution:
        """Solve the circuit at DC (capacitors open, inductors shorted)."""
        return self._solve(None)

    def solve_ac(self, frequency: float) -> CircuitSolution:
        """Solve the circuit at ``frequency`` hertz (phasor/steady-state)."""
        if frequency <= 0:
            raise ValueError("frequency must be positive")
        return self._solve(2 * math.pi * frequency)

    def equivalent_resistance(self, n1: int, n2: int) -> Quantity:
        """DC resistance seen between ``n1`` and ``n2`` (Thevenin, no sources).

        A 1 A test current is injected from ``n1`` to ``n2`` (using ``n2`` as
        the reference) and the resulting voltage is returned in ohms.
        """
        self._validate_nodes(n1, n2)
        if n1 == n2:
            raise ValueError("n1 and n2 must be different nodes")
        probe = Circuit(ground=n2)
        probe._elements = list(self._elements)
        probe.add_current_source(n1, n2, 1.0)
        solution = probe.solve_dc()
        drop = solution.voltage_phasor(n1) - solution.voltage_phasor(n2)
        return Quantity(abs(drop.real), OHM)
