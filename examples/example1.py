
from durapy.unimath import linalg

# --------------------------------------- #

vec1 = linalg.Vector([1, 2, 3])
vec2 = linalg.Vector([5, 6, 7])

vec3 = vec1 * vec2 # Dot product

print(vec3)

# --------------------------------------- #

mat1 = linalg.Matrix([[1, 2], [2, 1]])
mat2 = linalg.Matrix([[6, 1], [4, 7]])

mat3 = mat1 @ mat2 # Matrix multiplication

print(mat3)

# --------------------------------------- #
