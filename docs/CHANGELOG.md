# DURAPY CHANGELOG

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
