import time

import numpy as np

from durapy.unimath.linalg import Matrix

# Scale up to a size that requires heavy computing power
N = 10000
print(f"scale: {N}x{N}")
npa = np.random.rand(N, N).astype(np.float64)
npb = np.random.rand(N, N).astype(np.float64)

# Benchmark NumPy
start = time.perf_counter()
res_np = np.dot(npa, npb)
numpy_time = time.perf_counter() - start

dlxa = Matrix(array=npa.tolist())
dlxb = Matrix(array=npb.tolist())

# Benchmark DracoLIX (Fortran/Rust)
start = time.perf_counter()
res_dl = dlxa @ dlxb
dracolix_time = time.perf_counter() - start

print(f"NumPy Time:    {numpy_time:.6f} seconds")
print(f"DracoLIX Time: {dracolix_time:.6f} seconds")

# Assert correctness
assert np.allclose(res_np, np.array(res_dl.array)), "Mathematical mismatch detected!"
print("✅ Output validation passed successfully.")
