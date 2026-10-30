"""DuraPy Examples - UniMath basics"""

import numpy as np

from durapy.shared.constants import PI
from durapy.unimath import num_theory

# Vectors (NumPy)
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
print("v1 + v2 =", v1 + v2)
print("v1 . v2 (dot) =", v1 @ v2)
print("3 * v1 =", 3 * v1)

# Matrices (NumPy)
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print("\nA =", A)
print("A * B =", A @ B)
print("A^T =", A.T)
print("det(A) =", np.linalg.det(A))

# Constants / number theory
print("\npi =", PI)
print("factorial(5) =", num_theory.factorial(5))
print("gcd(48, 18) =", num_theory.gcd(48, 18))
print("lcm(4, 6) =", num_theory.lcm(4, 6))
print("fibonacci(10) =", num_theory.fibonacci_list(10))
