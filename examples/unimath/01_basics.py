"""DuraPy Examples - UniMath basics"""

from durapy.shared.constants import PI
from durapy.unimath import num_theory

# Constants / number theory
print("\npi =", PI)
print("factorial(5) =", num_theory.factorial(5))
print("gcd(48, 18) =", num_theory.gcd(48, 18))
print("lcm(4, 6) =", num_theory.lcm(4, 6))
print("fibonacci(10) =", num_theory.fibonacci_list(10))
