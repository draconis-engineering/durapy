# DuraPy — Remaining Findings (Medium severity)

TODO list of confirmed bug fixes, for after the 9 severe bugs are merged.
Each item was reproduced by running code against Python 3.14 (`PYTHONPATH=src`).

---

## 4. `d_mish` negative for negative inputs — NOT A BUG (false positive)

**File:** `src/durapy/unicogni/unicogni.py:123`

Resolved: the derivative is correct. Mish is **non-monotonic** (as its own
docstring states), so `d_mish` legitimately dips slightly negative around
`x ≈ -2.26`. Verified against a central-difference numerical derivative at
multiple points (see `tests/test_regressions.py::test_d_mish_matches_numeric_derivative`).
The original premise — "Mish is monotonically increasing" — is incorrect, so
**no code change was made.**

**Repro (now a passing regression guard):**

```python
import numpy as np
from durapy.unicogni.unicogni import d_mish
d_mish(np.array([-10.0]))   # -0.0004085... matches numeric derivative exactly
```

---

## 5. `cross_entropy_loss` fails on 1-D input — FIXED

**File:** `src/durapy/unicogni/unicogni.py:176`

Resolved: the axis is now derived from `ndim` (softmax/argmax over `axis=-1`),
so 1-D and N-D inputs both work, and probabilities are clipped for numerical
stability. Regression tests: `tests/test_regressions.py`.

---

## Notes

- Environment to reproduce: Python 3.14.6 via `PYTHONPATH=src`.
- `Matrix @ Matrix`, `Matrix @ Vector`, `Vector @ Matrix` via `@` all work correctly.
- Run the suite with `pytest` (configured in `pyproject.toml`).

## Fixed:

- [x] Matrix Scalar ops support for ints (was still float-only; now `Real` = int | float)
- [x] Rank only for square matrices (DracoLIX migration fix)
- [x] EMS gap 390-400
- [x] DMISH Negative error — investigated, formula is correct (Mish is non-monotonic)
- [x] Hardcoded CEL-axis — `cross_entropy_loss` now handles 1-D and N-D
- [x] Ohms law error fix
- [x] TotalESR fault - was already handled by a `ZeroDivisionError` guard
- [x] Bare except in unwrap_quantity
- [x] `binary_encrypt`/`otp_*` corrupted non-ASCII — now UTF-8 byte-correct
- [x] `vigenere_decrypt` crashed on empty key — now validated like encryption
- [x] `Unit.scale` was ignored — added `Quantity.to()` plus dimension-aware `+`, `-`, and comparisons

