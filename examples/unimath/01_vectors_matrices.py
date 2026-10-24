"""DuraPy Examples - UniMath basics"""

from durapy.unimath import linalg, num_theory
from durapy.shared.constants import PI

# Vectors
v1 = linalg.Vector([1, 2, 3])
v2 = linalg.Vector([4, 5, 6])
print("v1 + v2 =", v1 + v2)
print("v1 . v2 (dot) =", v1 * v2)
print("3 * v1 =", 3 * v1)

# Matrices
A = linalg.Matrix([[1, 2], [3, 4]])
B = linalg.Matrix([[5, 6], [7, 8]])
print("\nA =", A)
print("A * B =", A @ B)
print("A^T =", A.T)
print("det(A) =", A.det)

# Constants / number theory
print("\npi =", PI)
print("factorial(5) =", num_theory.factorial(5))
print("gcd(48, 18) =", num_theory.gcd(48, 18))
print("lcm(4, 6) =", num_theory.lcm(4, 6))
print("fibonacci(10) =", num_theory.fibonacci_list(10))
