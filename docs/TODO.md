# DuraPy — Remaining Findings (Medium severity)

TODO list of confirmed bug fixes, for after the 9 severe bugs are merged.
Each item was reproduced by running code against Python 3.14 (`PYTHONPATH=src`).

---

## 1. `Matrix` scalar ops reject `int`

**File:** `src/durapy/unimath/linalg.py:423-492`

`__add__`, `__sub__`, `__mul__`, `__truediv__`, `__rmul__` gate on `isinstance(other, float)`.
Python `int` is not a `float`, so `Matrix * 2`, `Matrix + 1`, `Matrix / 2`, `2 * Matrix` all raise `TypeError`.

**Repro:**
```python
Matrix([[1, 2], [3, 4]]) * 2   # TypeError: unsupported operand type(s)
```

**Fix:** accept `isinstance(other, (int, float))` in those dunders (use `numbers.Real`).

Related: `float - Matrix` is also broken — `__rsub__` (`linalg.py:464-467`) returns `NotImplemented` for any non-`Matrix`, so `1 - Matrix` raises `TypeError`. It should compute `other` scalar minus each element.

---

## 2. `rank` only works on square matrices

**File:** `src/durapy/unimath/linalg.py:737`

`rank` raises `ValueError("Matrix must be square to compute rank.")` for non-square input, but rank is well-defined for any shape (`min(rows, cols)` upper bound).

**Repro:**
```python
Matrix([[1, 2, 3], [4, 5, 6]]).rank   # ValueError
```

**Fix:** implement rank for general `M x N` matrices (e.g. gaussian-elimination pivot count or `np.linalg.matrix_rank`).

---

## 3. EM spectrum gap at 390–400 nm

**File:** `src/durapy/uniphys/electromagnetics.py:14` (with:29-51)

`EM_SPEC_WAVLEN` routes `[10, 400)` into `UV_SPEC_WAVLEN`, whose last band is `(315, 390)` (exclusive upper).
The visible map starts at 400. So wavelengths `390 <= λ < 400` fall through every band and `spectrum_label` raises `ValueError` ("out of range for this spectrum map"). 400 nm works, 399 and 390 don't.

**Repro:**
```python
from durapy.uniphys.electromagnetics import spectrum_label, EM_SPEC_WAVLEN
spectrum_label(395, EM_SPEC_WAVLEN)   # ValueError
```

**Fix:** change the UVA band to `(315, 400)` (physically correct: UVA = 315–400 nm), making `[390, 400)` resolve to Violet.

---

## 4. `d_mish` derivative is negative for negative inputs

**File:** `src/durapy/unicogni/unicogni.py:123`

Mish is monotonically increasing, so its derivative must be non-negative everywhere, but `d_mish` returns negative values for all `x < 0` (e.g. `d_mish(-10) ≈ -0.0004`). Formula bug in the mixed derivative.

**Repro:**
```python
import numpy as np
from durapy.unicogni.unicogni import d_mish
d_mish(np.array([-100.0, -10.0]))   # all negative below 0
```

**Fix:** use the correct Mish derivative
`ω = 4(x+1) + 4e^(2x) + e^(3x) + e^x(4x+6)`, `δ = 2e^x + e^(2x) + 2`,
`d = e^x * ω / δ²` — verify ≥ 0 on a range like `[-500, 500]`.

---

## 5. `cross_entropy_loss` fails on 1-D input

**File:** `src/durapy/unicogni/unicogni.py:176`

Hardcodes `axis=1`, so 1-D arrays raise `AxisError("axis 1 is out of bounds for array of dimension 1")`.

**Repro:**
```python
import numpy as np
cross_entropy_loss(np.array([1.0, 0.0, 0.0]), np.array([0.9, 0.05, 0.05]))   # AxisError
```

**Fix:** derive the softmax/cross-entropy axis from `ndim` (use `axis=-1` or handle 1-D explicitly) and add numerical-stability clipping.

---

## 6. `ohms_law` produces a confusing error for missing arguments

**File:** `src/durapy/unipower/unipower.py:54`

Calling `ohms_law(r=10)` (only one of v/i/r) raises a bare `TypeError` whose args are `(<function ohms_law at ...>, ['v', 'i'])` — a non-message. It should raise a clean, descriptive error listing the missing names.

**Repro:**
```python
ohms_law(r=10)   # TypeError (<function ohms_law at 0x...>, ['v', 'i'])
```

**Fix:** validate that exactly two of `v`/`i`/`r` are provided and raise `ValueError(f"ohms_law requires exactly two of v, i, r — missing: {missing}")`.

---

## 7. `total_esr` mishandles zero-ESR capacitors

**File:** `src/durapy/unipower/unipower.py:145`

A capacitor with `ESR = 0` short-circuits a parallel bank, so total parallel ESR must be `0`. Current code returns the parallel resistance of the non-zero caps (`[(100,50,0), (100,50,10)]` → `10.0 Ω`, should be `0 Ω`).

**Repro:**
```python
total_esr([(100, 50, 0), (100, 50, 10)], "parallel")   # 10 Ω, expected 0 Ω
```

**Fix:** if any ESR equals 0 in a parallel connection, return 0; also guard the all-zero case.

---

## 8. Bare `except:` in `_unwrap_quantity`

**File:** `src/durapy/shared/numval_types.py:132`

```python
except:  # line 132
```

Catches everything including `KeyboardInterrupt`/`SystemExit`. Should be narrowed to the expected exception types.

**Fix:** `except (TypeError, AttributeError):` (verify what `_unwrap_quantity` actually handles).

---

## 9. `tests/testbox.py` is a broken test, not a code bug

**File:** `tests/testbox.py`

The script expects `Matrix([[1, 2]]) @ Matrix([[1, 2]])` (1×2 @ 1×2, dimensionally invalid) to raise `ValueError` — that part works. But it doesn't wrap the call in `try/except`, so the raise kills the script before printing `"FAILED TO CATCH INVALID INPUT"`.

**Fix:** wrap in `try/except ValueError` and assert the failure message prints only when no exception is raised (convert to a `assert`/`pytest`-style check).

---

## Notes

- All 9 fixes above are independent of each other and of the already-fixed severe bugs.
- Environment to reproduce: `.\\.venv\\Scripts\\python.exe` (Python 3.14.6), run with `PYTHONPATH=src`.
- `Matrix @ Matrix`, `Matrix @ Vector`, `Vector @ Matrix` via `@` all work correctly after the earlier fixes (verified `[[1,2],[3,4]] @ [[1,0],[0,1]]`).
