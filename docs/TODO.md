# DuraPy — Remaining Findings

Status verified against the current working tree (`PYTHONPATH=src`, Python 3.14.6).
Severe bugs and the Medium-severity fixes below are committed/fixed.

## Deferred to DracoLIX (wontfix)

The entire `src/durapy/unimath/linalg.py` module is being deprecated and replaced by
the new DracoLIX engine, so these are intentionally left alone:

- **A. `scalar - Matrix`** — `linalg.py:464-467`; `__rsub__` advertises `Matrix | Real`
  but returns `NotImplemented` for non-Matrix, so `1 - Matrix` raises.
- **B. `rank` on non-square matrices** — `linalg.py:733-738`; helper `_rank`
  (696-731) is hardcoded to square (`N = rows = cols`).

---

## Fixed this round

### C. `d_mish` NaN for large positive input — FIXED
**File:** `src/durapy/unicogni/unicogni.py:123-133`

`np.exp` on an array overflows to `inf` (warning, **not** an `OverflowError`), so the
old `try/except OverflowError` was dead code and `d_mish(500)` returned `nan`.

**Fix:** `ex = np.exp(np.minimum(x, 20.0))` — for `x > 20` the derivative is `1` to
float precision, and the formula is unchanged below that. Verified: no NaN, large `x`
→ `1.0`, values for `x <= 20` byte-for-byte unchanged, no RuntimeWarning.

> Note: the negative values for `x < ~-1.2` are **correct** — Mish is non-monotonic
> by design. The earlier "negative derivative" framing was a false positive.

### D. `total_esr` mishandles zero-ESR capacitors (parallel) — FIXED
**File:** `src/durapy/unipower/unipower.py:154-163`

The old generator filtered out `ESR == 0`, so the `ZeroDivisionError` branch never ran
and a zero-ESR cap was silently ignored
(`[(100,50,0),(100,50,10)]` → `10 Ω` instead of `0 Ω`).

**Fix:** return `0 Ω` up front if any cap's ESR is 0 in a parallel bank. Verified:
mixed-zero → `0 Ω`, all-zero → `0 Ω`, normal `10||10` → `5 Ω`, series `0+10` → `10 Ω`.

---

## Previously fixed

1. **Matrix scalar ops reject `int`** — `+`, `*`, `/` now use `Real`. (`M*2`, `M+1`,
   `M/2` pass; `1-M` is deferred — see A.)
2. **EM spectrum gap 390–400 nm** — `electromagnetics.py`; `spectrum_label(390/395)` → Violet.
3. **`cross_entropy_loss` 1-D** — handles 1-D input.
4. **`ohms_law` missing-argument error** — raises a clear `TypeError` naming missing params.
5. **Bare `except:`** — `_unwrap_quantity` now catches `(TypeError, AttributeError)`.
6. **`tests/testbox.py`** — removed.
