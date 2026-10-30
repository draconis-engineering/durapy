"""DuraPy example: vectors and matrices with NumPy.

DuraPy no longer ships its own ``unimath.linalg`` module; use NumPy (or the
separate DracoLIX project) for linear algebra.
"""

import numpy as np

# --------------------------------------- #

vec1 = np.array([1, 2, 3])
vec2 = np.array([5, 6, 7])

dot = vec1 @ vec2  # Dot product

print(dot)

# --------------------------------------- #

mat1 = np.array([[1, 2], [2, 1]])
mat2 = np.array([[6, 1], [4, 7]])

mat3 = mat1 @ mat2  # Matrix multiplication

print(mat3)

# --------------------------------------- #
