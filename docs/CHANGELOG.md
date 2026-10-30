# DURAPY CHANGELOG

## 1.0.1.3 — 30.10.2026

### Security

- Replaced `sympy.sympify` on user-supplied expressions with a restricted,
  whitelisted parser (`unimath._parsing.parse_expression`), closing an
  arbitrary-code-execution hole in `algebra.derivative` and
  `trigonometry.tangent_formula`.
- Removed the `shell=True` subprocess call from `uniCLI.clear_terminal`; it now
  uses Rich's console clearing.

### Changed

- Removed the in-tree `unimath.linalg` module; use NumPy or DracoLIX for linear
  algebra. Examples and docs were updated accordingly.
- Physics helpers consolidated into `uniphys`; `unisky` keeps its domain API.
- Many functions now return `Quantity` objects.
- Switched the project license to GPL-3.0.

### Added

- Bernoulli, perfect-gas and rocket-thrust equations.
- New landing-page README, expanded runnable examples, and a pytest suite
  (136 tests).
- `SECURITY.md` and `CONTRIBUTING.md`.

### Fixed

- Assorted bug fixes (unit conversions, PID `dt`, numerical value types,
  naming and typing).

## 1.0.1.0 — 13.10.2026

### Added

- **UniPower component models** — every previously empty stub is now a real
  dataclass with validation and physics helpers:
  - `Capacitor` (charge, energy, time constant, reactance/impedance, rating)
  - `Inductor` (energy, time constant, reactance/impedance, resonance, rating)
  - `Diode` (Shockley current, piecewise-linear forward model, breakdown)
  - `Transistor` (BJT current gain, saturation, power, ratings)
  - `Potentiometer` (track halves, wiper voltage)
  - `Fuse`, `IC` and `Oscillator` (period, angular frequency, waveform sampling)
- **UniPower circuit solver** — `Circuit` implements modified nodal analysis
  (MNA) for DC and sinusoidal steady-state (AC/phasor) analysis:
  - `add_resistor` / `add_capacitor` / `add_inductor` / `add_voltage_source` /
    `add_current_source` and `add_component` for the component models
  - `solve_dc()` (capacitors open, inductors short), `solve_ac(frequency)` and
    `equivalent_resistance(n1, n2)`
  - `CircuitSolution` exposes node voltages and per-element currents
  - Raises `CircuitError` for singular/floating networks
- **UniPower AC/RLC analysis** (`durapy.unipower.ac`) — series/parallel
  combinations for R/L/C, reactance, complex RLC impedance (magnitude/phase),
  resonant frequency, series/parallel quality factor, bandwidth, RMS, decibel
  and dBm conversions, filter cut-offs/gains, and real/reactive/apparent power
  with power factor
- `Resistor.from_ohms(...)` for ideal construction plus `Resistor.power_dissipation(...)`
- New units: `HENRY` and `SIEMENS`
- `CircuitError` and `Element`/`CircuitSolution` exported from `durapy.unipower`
- `tests/test_unipower.py` — 33 tests covering the components, AC/RLC helpers
  and the circuit solver

## 12.10.2026

### Fixed

- `unimath.linalg.Matrix` scalar operations (`*`, `+`, `-`, `/`) now accept
  `int` as well as `float`, matching their type hints (used `Real = int | float`)
- `unicogni.cross_entropy_loss` now works on 1-D input by deriving the
  softmax/argmax axis from `ndim`, with probability clipping for stability
- `unicrypto.binary_encrypt`/`binary_decrypt` and `otp_encrypt`/`otp_decrypt`
  now operate on UTF-8 bytes, so non-ASCII text round-trips correctly
  (previously `ord()` + `08b` silently corrupted any codepoint above 255)
- `unicrypto.vigenere_decrypt` now validates the key (empty/non-alphabetic keys
  raised `ZeroDivisionError` before)
- `shared.numval_types`: `Unit.scale` is now honoured. Added
  `Quantity.to(unit)` and made `+`, `-`, and comparisons dimension-aware with
  automatic unit conversion; incompatible dimensions raise `UnitError`
  (a `ValueError` subclass)
- Corrected `docs/TODO.md`: the `d_mish` "bug" is a false positive — Mish is
  non-monotonic and the derivative matches the numerical derivative

### Added

- `tests/test_regressions.py` — regression coverage for every fix above
- **UniChem** — a new chemistry module
  - Full periodic table (118 elements) with `element()`, `atomic_mass()`, grouping helpers, and a `py.typed`-friendly `Element` dataclass
  - `parse_formula()` (nested parentheses + hydrates), `molar_mass()`, `mass_percent_composition()`, `empirical_formula()`
  - `balance_equation()` (preserves state labels), `percent_yield()`
  - `ideal_gas_law()` and solution chemistry: `molarity()`, `dilution()`, `ph()`, `poh()`, `henderson_hasselbalch()`
  - Dedicated exception hierarchy (`ChemistryError` and subclasses)

- **UniBio** — a new bioinformatics module
  - Sequence `normalize()`/`validate()`/`is_valid()` with IUPAC ambiguity support
  - `complement()`, `reverse_complement()`, `transcribe()`, `reverse_transcribe()`, `translate()`
  - `gc_content()`, `count_nucleotides()`, `hamming_distance()`, `melting_temperature()`, `molecular_weight()`
  - `find_orfs()` on both strands with an `ORF` result dataclass

- Test suite (`tests/test_unichem.py`, `tests/test_unibio.py`, `tests/test_regressions.py`)
- `Tests` GitHub Actions workflow across Python 3.11–3.13
- `py.typed` marker so downstream type checkers use DuraPy's annotations
- `[project.optional-dependencies].dev` and pytest configuration

## 29.07.2026

- Removed @requires_square decorator from `unimath`.`linalg`, since it messed up type checking
- Removed CuPy imports, since they are not universally supported. DracoLIX will soon be in charge of HPC anyway.

- Fixed some invalid __ init __ files to avoid things like "from durapy import unicli.unicli"

- Added stronger/consistent typing all troughout the DuraPy codebase
- Added input validation to `unimath`.`linalg` - especially for matrix operations, replacing the deficient requires_square decorators
