"""DuraPy Testbox"""

from durapy.unimath.linalg import Matrix

print("START")

# Mathematically invalid input case
A = Matrix([[1, 2]])
B = Matrix([[1, 2]])

print("INVALID INCOMING")
print(A @ B)
print("FAILED TO CATCH INVALID INPUT")

print("END")
