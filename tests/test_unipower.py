"""Tests for the UniPower module: component models, AC/RLC analysis and the
linear circuit solver."""

import math

import pytest

from durapy.unipower import (
    IC,
    Capacitor,
    Circuit,
    CircuitError,
    Diode,
    Fuse,
    Inductor,
    Oscillator,
    Potentiometer,
    Resistor,
    Transistor,
    apparent_power,
    bandwidth,
    capacitive_reactance,
    cutoff_frequency_rc,
    cutoff_frequency_rl,
    dbm_to_watts,
    decibels_amplitude,
    decibels_power,
    from_decibels,
    high_pass_magnitude,
    impedance_magnitude_phase,
    impedance_rlc,
    inductive_reactance,
    low_pass_magnitude,
    parallel_capacitance,
    parallel_inductance,
    parallel_quality_factor,
    parallel_resistance,
    power_factor,
    reactive_power,
    real_power,
    resonant_frequency,
    rms,
    rms_from_peak,
    series_capacitance,
    series_inductance,
    series_quality_factor,
    series_resistance,
    watts_to_dbm,
)
from durapy.unipower.types.circuit import Element

# --------------------------------------------------------------------------- #
# Component models
# --------------------------------------------------------------------------- #


def test_capacitor_physics():
    cap = Capacitor(2.0, voltage_rating=25.0)
    assert cap.charge(5.0).value == pytest.approx(10.0)
    assert cap.energy(5.0).value == pytest.approx(25.0)
    assert cap.time_constant(10.0).value == pytest.approx(20.0)
    assert cap.reactance(1000.0).value == pytest.approx(1 / (2 * math.pi * 1000 * 2))
    assert cap.impedance(1000.0) == pytest.approx(
        complex(0, -1 / (2 * math.pi * 1000 * 2))
    )
    assert cap.is_within_rating(24.0)
    assert not cap.is_within_rating(26.0)


def test_capacitor_validation():
    with pytest.raises(ValueError):
        Capacitor(0)
    with pytest.raises(ValueError):
        Capacitor(1e-6, voltage_rating=-1)
    with pytest.raises(ValueError):
        Capacitor(1e-6, esr=-1)


def test_inductor_physics():
    ind = Inductor(1e-3)
    assert ind.energy(2.0).value == pytest.approx(0.5 * 1e-3 * 4)
    assert ind.time_constant(10.0).value == pytest.approx(1e-4)
    assert ind.reactance(1000.0).value == pytest.approx(2 * math.pi * 1000 * 1e-3)
    assert ind.impedance(1000.0) == pytest.approx(complex(0, 2 * math.pi * 1000 * 1e-3))
    assert ind.resonant_frequency(1e-6).value == pytest.approx(
        1 / (2 * math.pi * math.sqrt(1e-3 * 1e-6))
    )


def test_inductor_validation():
    with pytest.raises(ValueError):
        Inductor(0)
    with pytest.raises(ValueError):
        Inductor(1e-3, current_rating=0)


def test_diode_model():
    diode = Diode(forward_voltage=0.7, breakdown_voltage=5.0)
    assert diode.thermal_voltage(300.0) == pytest.approx(0.02585, abs=1e-4)
    assert diode.shockley_current(0.0) == pytest.approx(0.0)
    assert diode.shockley_current(0.6) > 0
    assert diode.is_forward_biased(0.3)
    assert not diode.is_forward_biased(-0.3)
    assert diode.is_in_breakdown(-6.0)
    assert not diode.is_in_breakdown(-4.0)
    assert diode.forward_current(0.8, forward_resistance=10.0) == pytest.approx(0.01)
    assert diode.power_dissipation(0.02).value == pytest.approx(0.7 * 0.02)


def test_transistor_model():
    q = Transistor(beta=100.0, max_collector_current=0.1, max_power=0.5)
    assert q.collector_current(10e-6) == pytest.approx(1e-3)
    assert q.base_current(1e-3) == pytest.approx(1e-5)
    assert q.emitter_current(1e-5) == pytest.approx(101 * 1e-5)
    assert q.is_saturated(0.1)
    assert not q.is_saturated(5.0)
    assert q.power_dissipation(5.0, 1e-3).value == pytest.approx(5e-3)
    assert q.is_within_ratings(1e-3, 5.0)
    assert not q.is_within_ratings(0.2, 5.0)
    with pytest.raises(ValueError):
        Transistor(polarity="mosfet")


def test_potentiometer_model():
    pot = Potentiometer(total_resistance=10000.0, position=0.5)
    assert pot.bottom_resistance().value == pytest.approx(5000.0)
    assert pot.top_resistance().value == pytest.approx(5000.0)
    assert pot.wiper_voltage(0.0, 10.0).value == pytest.approx(5.0)
    assert Potentiometer(10000.0, 0.25).wiper_voltage(0.0, 10.0).value == pytest.approx(
        2.5
    )
    with pytest.raises(ValueError):
        Potentiometer(1000.0, 1.5)


def test_fuse_model():
    fuse = Fuse(rating_current=2.0)
    assert fuse.is_within_rating(2.0)
    assert fuse.will_blow(2.5)
    assert not fuse.will_blow(1.0)
    assert fuse.percent_loaded(1.0) == pytest.approx(50.0)
    with pytest.raises(ValueError):
        Fuse(0)


def test_ic_model():
    chip = IC(part_number="LM7805", pins=3, supply_min=0.0, supply_max=35.0)
    assert chip.is_within_supply(12.0)
    assert not chip.is_within_supply(40.0)
    assert chip.power_dissipation(12.0, 0.5).value == pytest.approx(6.0)
    with pytest.raises(ValueError):
        IC(supply_min=5.0, supply_max=3.0)


def test_oscillator_model():
    osc = Oscillator(frequency=100.0, amplitude=2.0)
    assert osc.period().value == pytest.approx(0.01)
    assert osc.angular_frequency().value == pytest.approx(2 * math.pi * 100)
    assert osc.value_at(1 / 400) == pytest.approx(2.0)  # sine peak (quarter period)
    square = Oscillator(100.0, 1.0, "square")
    assert square.value_at(0.0) == pytest.approx(1.0)
    assert square.value_at(0.006) == pytest.approx(-1.0)
    saw = Oscillator(100.0, 1.0, "sawtooth")
    assert saw.value_at(0.0) == pytest.approx(-1.0)
    with pytest.raises(ValueError):
        Oscillator(0.0)
    with pytest.raises(ValueError):
        Oscillator(100.0, waveform="cosine")


def test_resistor_from_ohms_and_power():
    resistor = Resistor.from_ohms(1000.0, tolerance=5.0)
    assert resistor.ohms.value == pytest.approx(1000.0)
    assert resistor.tolerance == pytest.approx(5.0)
    assert resistor.power_dissipation(voltage=10.0).value == pytest.approx(0.1)
    assert resistor.power_dissipation(current=0.01).value == pytest.approx(0.1)
    with pytest.raises(TypeError):
        resistor.power_dissipation()


def test_resistor_color_code_still_works():
    resistor = Resistor(("red", "red", "red", "gold", None))
    assert resistor.ohms.value == pytest.approx(2200.0)
    assert resistor.tolerance == pytest.approx(5.0)


# --------------------------------------------------------------------------- #
# AC / RLC helpers
# --------------------------------------------------------------------------- #


def test_series_and_parallel_resistance():
    assert series_resistance(1, 2, 3).value == pytest.approx(6.0)
    assert parallel_resistance(2, 2).value == pytest.approx(1.0)
    assert parallel_resistance(100, 100).value == pytest.approx(50.0)
    assert parallel_resistance(10, 0).value == pytest.approx(0.0)
    with pytest.raises(ValueError):
        series_resistance()


def test_capacitance_combinations():
    assert series_capacitance(1e-6, 1e-6).value == pytest.approx(0.5e-6)
    assert parallel_capacitance(1e-6, 2e-6).value == pytest.approx(3e-6)
    with pytest.raises(ValueError):
        series_capacitance(0)


def test_inductance_combinations():
    assert series_inductance(1e-3, 2e-3).value == pytest.approx(3e-3)
    assert parallel_inductance(1e-3, 1e-3).value == pytest.approx(0.5e-3)
    with pytest.raises(ValueError):
        parallel_inductance(0)


def test_reactances():
    assert capacitive_reactance(1000.0, 1e-6).value == pytest.approx(
        1 / (2 * math.pi * 1000 * 1e-6)
    )
    assert inductive_reactance(1000.0, 1e-3).value == pytest.approx(
        2 * math.pi * 1000 * 1e-3
    )
    with pytest.raises(ValueError):
        capacitive_reactance(0, 1e-6)


def test_impedance_rlc_and_resonance():
    l, c = 1e-3, 1e-6
    f0 = resonant_frequency(l, c).value
    assert f0 == pytest.approx(1 / (2 * math.pi * math.sqrt(l * c)))
    z = impedance_rlc(f0, 10.0, l, c)
    assert z == pytest.approx(complex(10.0, 0.0), abs=1e-6)
    magnitude, phase = impedance_magnitude_phase(complex(3, 4))
    assert magnitude == pytest.approx(5.0)
    assert phase == pytest.approx(53.130102, abs=1e-5)


def test_quality_factor_and_bandwidth():
    l, c, r = 1e-3, 1e-6, 10.0
    qs = series_quality_factor(r, l, c)
    assert qs == pytest.approx((1 / r) * math.sqrt(l / c))
    qp = parallel_quality_factor(r, l, c)
    assert qp == pytest.approx(r * math.sqrt(c / l))
    assert bandwidth(1000.0, 10.0).value == pytest.approx(100.0)


def test_power_relationships():
    assert power_factor(60.0) == pytest.approx(0.5)
    assert apparent_power(10.0, 2.0).value == pytest.approx(20.0)
    assert real_power(10.0, 2.0, 60.0).value == pytest.approx(10.0)
    assert reactive_power(10.0, 2.0, 60.0).value == pytest.approx(10 * math.sqrt(3))


def test_rms_and_decibels():
    assert rms([3, 4]) == pytest.approx(math.sqrt(12.5))
    assert rms_from_peak(10.0) == pytest.approx(10 / math.sqrt(2))
    assert decibels_power(100.0) == pytest.approx(20.0)
    assert decibels_amplitude(10.0) == pytest.approx(20.0)
    assert from_decibels(20.0) == pytest.approx(100.0)
    assert from_decibels(20.0, amplitude=True) == pytest.approx(10.0)
    assert dbm_to_watts(30.0).value == pytest.approx(1.0)
    assert watts_to_dbm(1.0) == pytest.approx(30.0)
    with pytest.raises(ValueError):
        rms([])


def test_filter_cutoffs():
    assert cutoff_frequency_rc(1000.0, 1e-6).value == pytest.approx(
        1 / (2 * math.pi * 1000 * 1e-6)
    )
    assert cutoff_frequency_rl(1000.0, 1e-3).value == pytest.approx(
        1000 / (2 * math.pi * 1e-3)
    )
    assert low_pass_magnitude(0.0, 100.0) == pytest.approx(1.0)
    assert low_pass_magnitude(100.0, 100.0) == pytest.approx(1 / math.sqrt(2))
    assert high_pass_magnitude(100.0, 100.0) == pytest.approx(1 / math.sqrt(2))


# --------------------------------------------------------------------------- #
# Circuit solver
# --------------------------------------------------------------------------- #


def test_voltage_divider_dc():
    circuit = Circuit()
    circuit.add_voltage_source(1, 0, 10.0)
    circuit.add_resistor(1, 2, 1000.0)
    r2 = circuit.add_resistor(2, 0, 1000.0)
    solution = circuit.solve_dc()
    assert solution.voltage(2).value == pytest.approx(5.0)
    assert solution.current(r2).value == pytest.approx(5e-3)
    assert solution.voltage(0).value == pytest.approx(0.0)


def test_parallel_equivalent_resistance():
    circuit = Circuit()
    circuit.add_resistor(1, 0, 100.0)
    circuit.add_resistor(1, 0, 100.0)
    assert circuit.equivalent_resistance(1, 0).value == pytest.approx(50.0)


def test_series_equivalent_resistance():
    circuit = Circuit()
    circuit.add_resistor(1, 2, 100.0)
    circuit.add_resistor(2, 0, 100.0)
    assert circuit.equivalent_resistance(1, 0).value == pytest.approx(200.0)


def test_current_source_dc():
    circuit = Circuit()
    circuit.add_current_source(1, 0, 1e-3)
    resistor = circuit.add_resistor(1, 0, 1000.0)
    solution = circuit.solve_dc()
    assert solution.voltage(1).value == pytest.approx(1.0)
    assert solution.current(resistor).value == pytest.approx(1e-3)


def test_inductor_is_short_in_dc():
    circuit = Circuit()
    circuit.add_voltage_source(1, 0, 5.0)
    inductor = circuit.add_inductor(1, 2, 1e-3)
    circuit.add_resistor(2, 0, 100.0)
    solution = circuit.solve_dc()
    assert solution.voltage(2).value == pytest.approx(5.0)
    assert solution.current(inductor).value == pytest.approx(0.05)


def test_capacitor_is_open_in_dc():
    circuit = Circuit()
    circuit.add_voltage_source(1, 0, 5.0)
    circuit.add_resistor(1, 2, 1000.0)
    circuit.add_capacitor(2, 0, 1e-6)
    solution = circuit.solve_dc()
    # no DC path through the capacitor -> node 2 pulled to 5 V through R
    assert solution.voltage(2).value == pytest.approx(5.0)


def test_rc_low_pass_at_cutoff_ac():
    r, c = 1000.0, 1e-6
    fc = 1 / (2 * math.pi * r * c)
    circuit = Circuit()
    circuit.add_voltage_source(1, 0, 1.0)
    circuit.add_resistor(1, 2, r)
    circuit.add_capacitor(2, 0, c)
    solution = circuit.solve_ac(fc)
    assert abs(solution.voltage_phasor(2)) == pytest.approx(1 / math.sqrt(2), rel=1e-6)


def test_series_rlc_resonance_ac():
    l, c, r = 1e-3, 1e-6, 10.0
    f0 = 1 / (2 * math.pi * math.sqrt(l * c))
    circuit = Circuit()
    circuit.add_voltage_source(1, 0, 1.0)
    resistor = circuit.add_resistor(1, 2, r)
    circuit.add_inductor(2, 3, l)
    circuit.add_capacitor(3, 0, c)
    solution = circuit.solve_ac(f0)
    current = abs(solution.current_phasor(resistor))
    assert current == pytest.approx(1.0 / r, rel=1e-6)


def test_add_component_models():
    circuit = Circuit()
    circuit.add_voltage_source(1, 0, 5.0)
    circuit.add_component(Resistor.from_ohms(1000.0), 1, 2)
    circuit.add_component(Inductor(1e-3), 2, 3)
    circuit.add_component(Capacitor(1e-6), 3, 0)
    solution = circuit.solve_dc()
    assert solution.voltage(2).value == pytest.approx(5.0)


def test_singular_circuit_raises():
    circuit = Circuit()  # ground 0 is never connected
    circuit.add_resistor(1, 2, 100.0)
    with pytest.raises(CircuitError):
        circuit.solve_dc()


def test_circuit_validation():
    circuit = Circuit()
    with pytest.raises(ValueError):
        circuit.add_resistor(1, 1, 100.0)
    with pytest.raises(ValueError):
        circuit.add_resistor(-1, 0, 100.0)
    with pytest.raises(ValueError):
        circuit.add_resistor(1, 0, 0.0)
    with pytest.raises(ValueError):
        Circuit(ground=-1)


def test_solution_rejects_foreign_element():
    circuit = Circuit()
    circuit.add_resistor(1, 0, 100.0)
    solution = circuit.solve_dc()
    with pytest.raises(CircuitError):
        solution.current(Element("R", 1, 0, 100.0))
