# DuraPy — Remaining Findings (Medium severity)

TODO list of confirmed bug fixes, for after the 9 severe bugs are merged.
Each item was reproduced by running code against Python 3.14 (`PYTHONPATH=src`).

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

## Notes

- All 9 fixes above are independent of each other and of the already-fixed severe bugs.
- Environment to reproduce: `.\\.venv\\Scripts\\python.exe` (Python 3.14.6), run with `PYTHONPATH=src`.
- `Matrix @ Matrix`, `Matrix @ Vector`, `Vector @ Matrix` via `@` all work correctly after the earlier fixes (verified `[[1,2],[3,4]] @ [[1,0],[0,1]]`).

## Fixed:

- [x] Matrix Scalar ops support for ints (DracoLIX Migration fix)
- [x] Rank only for square matrices (DracoLIX migration fix)
- [x] EMS gap 390-400
- [?] DMISH Negative error - the formula is correct?
- [ ] Hardcoded CEL-axis
- [x] Ohms law error fix
- [.] TotalESR fault - was already handled by a `ZeroDivisionError` guard
- [x] Bare except in unwrap_quantity
