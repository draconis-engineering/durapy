"""DuraPy Testbox I"""

import numpy as np
from durapy.unimath.linalg import Matrix, Vector

print("START")

vec1 = Vector(components=[1, 2, 3])
print("\nvec1 | type: ", type(vec1))
print(vec1)

vec2 = np.array([1, 2, 3])
print("\nvec2 | type: ", type(vec2))
print(vec2)

mat1 = Matrix(array=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\nmat1 | type: ", type(mat1))
print(mat1)

mat2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\nmat2 | type: ", type(mat2))
print(mat2)

matvec1 = mat1 @ vec1
print("\nmatvec1 | type: ", type(matvec1))
print(matvec1)

matvec2 = mat2 @ vec2
print("\nmatvec2 | type: ", type(matvec2))
print(matvec2)

matmat1 = mat1 @ mat1
print("\nmatmat1 | type: ", type(matmat1))
print(matmat1)

matmat2 = mat2 @ mat2
print("\nmatmat2 | type: ", type(matmat2))
print(matmat2)

vecvec1 = vec1 * vec1
print("\nvecvec1 | type: ", type(vecvec1))
print(vecvec1)

vecvec2 = vec2 @ vec2
print("\nvecvec2 | type: ", type(vecvec2))
print(vecvec2)

# VecMat multiplication needs to define if it is row- or column-based

vecmat1 = vec1 @ mat1
print("\nvecmat1 | type: ", type(vecmat1))
print(vecmat1)

vecmat2 = vec2 @ mat2
print("\nvecmat2 | type: ", type(vecmat2))
print(vecmat2)

print("END")
