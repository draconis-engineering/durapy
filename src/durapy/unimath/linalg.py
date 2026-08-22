"""
`UniMath` Linear Algebra source

Data Types
----------

`NDVector` - N-dimensional vector.

`Matrix` - N*M-matrix.

`D4Tensor` - 4-dimensional tensor (A matrix of matrices)
"""

from __future__ import annotations

import copy
import math
import random
from collections.abc import Sequence
from typing import overload, override

import numpy as np
from dracolix import matmatmul, matvecmul  # type: ignore missing pyi files

EPSILON = 1e-9

Real = int | float
Scalar = int | float | complex
Numerical = int | float | complex | np.ndarray | list[float] | list[list[float]]


def is_close(a: Numerical, b: Numerical) -> bool:
    """Checks if two floats / list-like objects of floats are close"""

    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b)

    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False

        return all(is_close(x, y) for x, y in zip(a, b))

    if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
        return np.allclose(a, b)

    return False


class Vector:
    """
    `DuraPy` Dataclass for N-dimensional vectors.

    Args
    ----
    `components`: list[float] - The components of the vector, in order.
    """

    def __init__(self, components: Sequence[Scalar]):
        self.components: list[Scalar] = list(components)
        self.real_components: list[float] = [
            component.real for component in self.components
        ]
        self.imag_components: list[float] = [
            component.imag for component in components if component.imag != 0
        ]
        # self.is_row_vec = False
        # self.is_col_vec = False

    @property
    def magnitude(self) -> float:
        """The magnitude (length) of the vector. Uses the real components only."""
        return math.hypot(*self.real_components)

    @property
    def shape(self) -> tuple[int, int]:
        """The shape (dimension) of the vector."""
        return (len(self.components), 1)

    def __getitem__(self, idx: int) -> Scalar:
        return self.components[idx]

    def __setitem__(self, key: int, value: Scalar) -> None:
        temp = list(self.components)
        temp[key] = value
        self.components = temp

    def __iter__(self):
        return iter(self.components)

    @override
    def __repr__(self) -> str:
        return f"<Vector{(component for component in self.components)}>"

    @override
    def __str__(self) -> str:
        return str(self.components).replace(",", "")

    def __abs__(self) -> Vector:
        return Vector([abs(component) for component in self.components])

    def __len__(self) -> int:
        return len(self.components)

    def __neg__(self) -> Vector:
        return Vector([-(component) for component in self.components])

    @override
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Vector):
            return self.components == value.components and self.shape == value.shape
        if isinstance(value, list):
            return self.components == value
        return NotImplemented

    @overload
    def __add__(self, other: Real) -> Vector: ...
    @overload
    def __add__(self, other: Vector) -> Vector: ...
    def __add__(self, other: object) -> Vector:
        if isinstance(other, Real):  # scalar addition
            return Vector(
                [self.components[i] + other for i in range(len(self.components))]
            )
        if isinstance(other, Vector):  # vector addition
            if self.shape[0] != other.shape[0]:
                raise ValueError("Vectors must have the same length for addition")
            return Vector(
                [
                    self.components[i] + other.components[i]
                    for i in range(len(self.components))
                ]
            )
        return NotImplemented

    def __radd__(self, other: Real | Vector) -> Vector:
        return self.__add__(other)

    @overload
    def __sub__(self, other: Real) -> Vector: ...
    @overload
    def __sub__(self, other: Vector) -> Vector: ...
    def __sub__(self, other: object) -> Vector:
        if isinstance(other, Real):  # scalar subtraction
            if len(self.components) != 1:
                raise ValueError("Scalar subtraction is only supported for 1D vectors")

            return Vector(
                [self.components[i] - other for i in range(len(self.components))]
            )
        if isinstance(other, Vector):  # vector subtraction
            if self.shape[0] != other.shape[0]:
                raise ValueError("Vectors must have the same length for subtraction")

            return Vector(
                [
                    self.components[i] - other.components[i]
                    for i in range(len(self.components))
                ]
            )
        return NotImplemented

    def __rsub__(self, other: Vector) -> Vector:
        return other.__sub__(self)

    @overload
    def __mul__(self, other: Real) -> Vector: ...
    @overload
    def __mul__(self, other: Vector) -> float: ...
    def __mul__(self, other: object) -> Vector | float:
        if isinstance(other, Real):  # scalar multiplication
            if len(self.components) != 1:
                raise ValueError(
                    "Scalar multiplication is only supported for 1D vectors"
                )
            return Vector(
                [other * self.components[i] for i in range(len(self.components))]
            )
        if isinstance(other, Vector):  # vector multiplication | Dot product
            if self.shape[0] != other.shape[0]:
                raise ValueError("Vectors must have the same length for dot product")
            return np.dot(
                np.array(self.components), np.array(other.components)
            )  ### MIGRATE TO DRACOLIX WHEN IMPLEMENTED

        return NotImplemented

    def __rmul__(self, other: Real) -> Vector:
        return self.__mul__(other)

    @overload
    def __truediv__(self, other: Real) -> Vector: ...
    @overload
    def __truediv__(self, other: Vector) -> Vector: ...
    def __truediv__(self, other: object) -> Vector:
        if isinstance(other, Real):  # scalar division
            return Vector([component / other for component in self.components])
        if isinstance(other, Vector):  # vector division
            if self.shape[0] != other.shape[0]:
                raise ValueError("Vectors must have the same length for division")
            return Vector([x / y for x, y in zip(self.components, other.components)])
        return NotImplemented

    def __rtruediv__(self, other: Vector) -> Vector:
        return other.__truediv__(self)

    @overload
    def __matmul__(self, other: Vector) -> Vector: ...
    @overload
    def __matmul__(self, other: Matrix) -> Matrix: ...
    def __matmul__(self, other: object) -> Vector | Matrix:
        if isinstance(other, Vector):  # Outer product
            if self.shape[1] != other.shape[0]:
                raise ValueError("Matrix dimensions do not match for multiplication")
            return Matrix(
                array=list(
                    np.outer(  ### MIGRATE TO DRACOLIX WHEN IMPLEMENTED
                        np.array(self.components), np.array(other.components)
                    ).tolist()
                )
            )
        if isinstance(other, Matrix):
            if self.shape[1] != other.shape[0]:
                raise ValueError(
                    "Matrix dimensions do not match for multiplication"
                )  ### MIGRATE TO DRACOLIX WHEN IMPLEMENTED
            return Matrix(
                array=list(
                    np.vecmat(
                        np.array(self.components), np.array(other.array)
                    )  ### MIGRATE TO DRACOLIX WHEN IMPLEMENTED
                )
            )
        return NotImplemented

    @overload
    def __rmatmul__(self, other: Vector) -> Vector: ...
    @overload
    def __rmatmul__(self, other: Matrix) -> Matrix: ...
    def __rmatmul__(self, other: Vector | Matrix) -> Vector | Matrix:
        return other.__matmul__(self)


### NOTE | Functions are split into functions and properties to bypass the effects of @requires_square, since it messes up type hints


class Matrix:
    def __init__(
        self,
        array: list[list[float]] | None = None,
        shape: tuple[int, int] | None = None,
        randomfill: bool | None = False,
        randrange: tuple[float, float] = (-1, 1),
        fill: float = 0.0,
    ) -> None:
        """
        N*M-dimensional Matrix.

        Args
        ----
        `array`: list[list[float]] - The data to create the matrix from, unless empty or random values are preferred.

        `shape`: tuple[int, int] - Create an empty matrix with dimensions `Rows` x `Cols`

        `randomfill`: bool - Create a matrix filled with uniform values ranging from -1 and 1 unless otherwise specified with the `randrange` parameter.

        `randtype`: type - Specifies if the matrix should be filled with random integers or floats.

        `randrange`: tuple - Specifies the range for the `random`.`uniform` function.

        `fill`: float - Specifies what value to fill the matrix with, if not random.
        """
        if shape == (0, 0):
            raise ValueError("Matrix can't have 0 rows or columns!")

        if array:
            if shape:
                raise ValueError(
                    "Both array and size parameters are provided! Only one should be specified."  # Make this config valid, by taking the array and reshaping it into the specified shape
                )
            if len(array) == 0 or any(len(row) != len(array[0]) for row in array):
                raise ValueError("Matrix must be rectangular and non-empty")
        else:
            if not shape:
                raise ValueError(
                    "Missing array and size parameters! Matrix() needs atleast 1!"
                )

        if not array and shape:
            rows, cols = shape
            if randomfill:
                array = [
                    [random.uniform(*randrange) for _ in range(cols)]
                    for _ in range(rows)
                ]
            else:
                array = [[fill for _ in range(cols)] for _ in range(rows)]

        self._array: list[list[float]] = array if array else [[0.0, 0.0], [0.0, 0.0]]
        self._rows: int = len(self._array)
        self._cols: int = len(self._array[0]) if self._rows > 0 else 0

    @property
    def array(self) -> list[list[float]]:
        """Returns the matrix as a list of lists."""
        return self._array

    @property
    def shape(self) -> tuple[int, int]:
        """Returns the dimensions of the matrix in the format: (`rows`,`cols`)"""
        return self._rows, self._cols

    @property
    def elements(self) -> int:
        """Returns the total number of elements in the matrix."""
        return self._rows * self._cols

    @property
    def zeroes(self) -> int:
        """Returns the number of elements which are zero."""
        zero = 0
        for row in self._array:
            for element in row:
                zero += 1 if math.isclose(element, 0) else 0
        return zero

    @property
    def nonzeroes(self) -> int:
        """Returns the number of elements which are not zero."""
        nonzero = 0
        for row in self._array:
            for element in row:
                nonzero += 1 if not math.isclose(element, 0) else 0
        return nonzero

    def __getitem__(self, idx: int) -> list[float]:
        if idx < 0 or idx > self.shape[0]:
            raise IndexError("Key out of bounds!")
        return self._array[idx]

    def __setitem__(self, key: int, value: list[float]) -> None:
        if key < 0 or key > self.shape[0]:
            raise IndexError("Key out of bounds!")
        if len(value) != self._cols:
            raise ValueError(
                "New row length doesn't match the dimensions of the matrix!"
            )
        self._array[key] = value

    def set_row(self, idx: int, new_row: list[float]) -> None:
        if len(new_row) != self._cols:
            raise ValueError(
                "New row length doesn't match the dimensions of the matrix!"
            )
        self[idx] = new_row

    def row(self, idx: int) -> list[float]:
        return self[idx]

    def set_column(self, idx: int, new_col: list[float]) -> None:
        if len(new_col) != self._rows:
            raise ValueError(
                "New column length doesn't match the dimensions of the matrix!"
            )

        for j in range(len(self._array)):
            self[j][idx] = new_col[j]

    def column(self, idx: int) -> list[float]:
        return [self[j][idx] for j in range(len(self))]

    def to_row_vectors(self) -> list[Vector]:
        return [Vector(components=row) for row in self]

    def to_column_vectors(self) -> list[Vector]:
        return [Vector(components=column) for column in self.T]

    def __bool__(self) -> bool:
        return any(any(cell != 0 for cell in row) for row in self._array)

    def __iter__(self):
        return iter(self._array)

    @override
    def __repr__(self) -> str:
        return f"Matrix({self._array!r})"

    @override
    def __str__(self) -> str:
        return_str = ""
        for row in self:
            return_str += str(row).replace(",", "") + "\n"

        return return_str

    def __neg__(self) -> Matrix:
        return Matrix(
            [
                [-(self[idx1][idx2]) for idx2 in range(self._cols)]
                for idx1 in range(self._rows)
            ]
        )

    def __len__(self) -> int:
        return self._rows * self._cols

    def __abs__(self) -> float:
        return math.sqrt(sum(cell * cell for row in self._array for cell in row))

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Matrix):
            return (
                is_close(self._array, other._array)
                and self._rows == other._rows
                and self._cols == other._cols
            )
        else:
            return self._array == other

    def __add__(self, other: Matrix | float) -> Matrix:
        if isinstance(other, Matrix):
            if self.shape != other.shape:
                raise ValueError("Matrix summation only takes same-size dimensions!")
            return Matrix(
                [
                    [self[i][j] + other[i][j] for j in range(self._cols)]
                    for i in range(self._rows)
                ]
            )
        elif isinstance(other, float):
            return Matrix(
                [
                    [self[i][j] + other for j in range(self._cols)]
                    for i in range(self._rows)
                ]
            )
        return NotImplemented

    def __radd__(self, other: Matrix | float) -> Matrix:
        return self.__add__(other)

    def __sub__(self, other: Matrix | float) -> Matrix:
        if isinstance(other, Matrix):
            if self._rows != other._rows or self._cols != other._cols:
                raise ValueError("Matrix subtraction only takes same-size dimensions!")
            return Matrix(
                [
                    [self[i][j] - other[i][j] for j in range(self._cols)]
                    for i in range(self._rows)
                ]
            )
        elif isinstance(other, float):
            return Matrix(
                [
                    [self[i][j] - other for j in range(self._cols)]
                    for i in range(self._rows)
                ]
            )
        return NotImplemented

    def __rsub__(self, other: Matrix | float) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented  # Cant subtract a matrix from a int/float
        return other.__sub__(self)

    def __mul__(self, other: float) -> Matrix:
        if isinstance(other, float):
            return Matrix(
                [
                    [self[i][j] * other for j in range(self._cols)]
                    for i in range(self._rows)
                ]
            )
        return NotImplemented

    def __rmul__(self, other: float) -> Matrix:
        if isinstance(other, float):
            return self.__mul__(other)  # Commutative
        return NotImplemented

    def __truediv__(self, other: float) -> Matrix:
        if isinstance(other, float):
            return Matrix(
                [
                    [self[i][j] / other for j in range(self._cols)]
                    for i in range(self._rows)
                ]
            )
        return NotImplemented

    @overload
    def __matmul__(self, other: Matrix) -> Matrix: ...
    @overload
    def __matmul__(self, other: Vector) -> Vector: ...
    def __matmul__(self, other: object) -> Matrix | Vector:
        if isinstance(other, Matrix):
            if self._cols != other._rows:
                raise ValueError("Matrix dimensions do not match for multiplication")

            return Matrix(
                array=list(
                    matmatmul(
                        np.array(self._array, dtype=np.float64),
                        np.array(other._array, dtype=np.float64),
                    )
                )
            )

        if isinstance(other, Vector):
            if self._cols != other.shape[0]:
                raise ValueError("Matrix dimensions do not match for multiplication")

            return Vector(
                components=list(
                    matvecmul(
                        np.array(self._array, dtype=np.float64),
                        np.array(other.components, dtype=np.float64),
                    )
                )
            )

        return NotImplemented

    @overload
    def __rmatmul__(self, other: Matrix) -> Matrix: ...
    @overload
    def __rmatmul__(self, other: Vector) -> Vector: ...
    def __rmatmul__(self, other: Matrix | Vector) -> Matrix | Vector:
        return other.__matmul__(self)

    def _T(self) -> Matrix:
        """Helper method to compute the transpose of the matrix."""
        rows, cols = self.shape
        transpose = Matrix(shape=(cols, rows))
        for i in range(rows):
            for j in range(cols):
                transpose[i][j] = self[j][i]

        return transpose

    @property
    def T(self) -> Matrix:
        """
        Returns the transposed matrix of itself.

        A transposed matrix is the original matrix but with its rows and columns swapped,
        so one element in the original matrix - `A[I][J]` becomes `A[J][I]` in the transpose.
        It is as if the matrix was rotated around its diagonal from the top-left to bottom-right.
        """
        return self._T()

    def is_square(self) -> bool:
        """Returns if the matrix is square (rows = columns). Decides if the matrix has certain properties, like determinant, inverse, etc."""
        return self._cols == self._rows

    @staticmethod
    def __sign(expr: float, idx: int) -> float:
        """Helper method to compute the sign of an expression based on the index."""
        return expr * (-(1.0**idx))

    @staticmethod
    def __2x2_det(_array: list[list[float]]) -> float:
        """Helper method to compute the determinant of a 2x2 matrix."""

        if len(_array) == 2 and all(len(row) == 2 for row in _array):
            A, B, C, D = _array[0][0], _array[0][1], _array[1][0], _array[1][1]
            return (A * D) - (B * C)
        raise ValueError(
            "Can't calculate a base case 2x2 determinant of a non-2x2 matrix!"
        )

    @staticmethod
    def __minor_extract(arr: list[list[float]], row_idx: int, col_idx: int) -> Matrix:
        """Helper method to extract the minor matrix by removing the specified row and column from the given array."""

        without_row = [arr[idx] for idx in range(len(arr)) if idx != row_idx]
        without_col = [
            [
                without_row[idx1][idx2]
                for idx2 in range(len(without_row[idx1]))
                if idx2 != col_idx
            ]
            for idx1 in range(len(without_row))
        ]
        return Matrix(array=without_col)

    @staticmethod
    def _det(M: Matrix) -> float:
        """Helper method to compute the determinant of the matrix through Laplace Expansion."""

        if M.shape[0] == 2:
            return M.__2x2_det(M._array)
        if M.shape[0] == 1:
            return M._array[0][0]

        detsum = 0.0

        for idx1, _ in enumerate(M[0]):
            minor = M.__minor_extract(M._array, 0, idx1)
            detsum += M.__sign(M[0][idx1] * M._det(minor), idx1)

        return detsum

    @property
    def det(self) -> float:
        """
        Returns the determinant of the matrix through Laplace Expansion.

        The determinant is used to determine if the Matrix is invertible or singular (collapses space).
        """
        if not self.is_square():
            raise ValueError("Matrix must be square to compute determinant.")
        return self._det(self)

    def __build_augmented(self) -> Matrix:
        """Builds the augmented matrix by concatenating the original matrix with its identity matrix."""
        n = self.shape[0]
        i = self.to_identity

        aug = Matrix(
            array=[[0.0 for _ in range(2 * n)] for _ in range(n)],
        )

        for j in range(n):
            for k in range(n):
                aug[j][k] = self[j][k]
                aug[j][k + n] = i[j][k]

        return aug

    def _inverse(self) -> Matrix | None:
        """Helper method to compute the inverse of the matrix."""

        # Check if the determinant is zero, indicating the matrix is singular and cannot be inverted
        if self.det == 0:
            return None

        # Build the augmented matrix
        n, _ = self.shape
        aug = self.__build_augmented()

        # Gaussian Elimination to transform the augmented matrix into reduced row echelon form
        for i in range(n):
            pivot = aug[i][i]

            # Find a non-zero pivot in the current column
            if pivot == 0:
                for j in range(i + 1, n):
                    # Swap rows to bring a non-zero pivot into the current row
                    if aug[j][i] != 0:
                        aug[i], aug[j] = aug[j], aug[i]
                        pivot = aug[i][i]
                        break

            # If no non-zero pivot is found, return None
            if pivot == 0:
                return None

            # Scale the pivot row to make the pivot element 1
            aug[i] = [x / pivot for x in aug[i]]

            # Row reduction to eliminate the pivot column in other rows
            for j in range(n):
                if j != i:
                    factor = aug[j][i]
                    aug[j] = [aug[j][k] - factor * aug[i][k] for k in range(2 * n)]

        return Matrix(array=[row[n:] for row in aug])

    @property
    def inverse(self) -> Matrix | None:
        """
        Returns the inverse of the matrix through Gauss-Jordan elimination.

        The inverse of a matrix `A`, `A^-1`, satisfies the following equation:

        `A` * `A^-1` = `A^-1` * `A` = `I`,

        where `I` is the identity matrix of the same dimensions.
        """
        if not self.is_square():
            raise ValueError("Matrix must be square to compute inverse.")

        return self._inverse()

    def _rank(self) -> int:
        """
        Returns the rank of the matrix via Gaussian Elimination.

        The rank is the number of linearly independent rows or columns in the matrix.
        """
        A = copy.deepcopy(self)
        N = A.shape[0]

        rank, row_idx = N, 0

        # Iterate over each column to find pivot rows and eliminate non-zero elements below
        for col in range(N):
            pivot_row_idx = row_idx

            # Skip rows that are already zero in this column
            while pivot_row_idx < N and abs(A[pivot_row_idx][col]) < EPSILON:
                pivot_row_idx += 1

            # If no pivot row is found, skip this column
            if pivot_row_idx == N:
                rank -= 1
                continue

            # Swap pivot row with current row if necessary
            if pivot_row_idx != row_idx:
                A[row_idx], A[pivot_row_idx] = A[pivot_row_idx], A[row_idx]  # Swap

            # Eliminate non-zero elements below the pivot row
            for i in range(row_idx + 1, N):
                factor = A[i][col] / A[row_idx][col]

                # Subtract the factor times the pivot row from the current row
                for J in range(col, N):
                    A[i][J] -= factor * A[row_idx][J]

            row_idx += 1

            # Check if we've reached the end of the matrix
            if row_idx == N:
                break

        return rank

    @property
    def rank(self) -> int:
        """The Matrix Rank. Uses Gaussian Elimination to find the number of linearly independent rows."""
        if not self.is_square():
            raise ValueError("Matrix must be square to compute rank.")
        return self._rank()

    @staticmethod
    def __QR_decomp(A: Matrix) -> tuple[Matrix, Matrix]:
        """QR decomposition via modified Gram-Schmidt process."""
        N = A.shape[0]
        Q = Matrix(shape=(N, N))
        R = Matrix(shape=(N, N))

        # Iteratively build Q and R matrices
        for J in range(N):
            v = A.column(J)

            # Orthogonalize v against previous columns in Q
            for i in range(J):
                QI = Q.column(i)
                R[i][J] = sum(x * y for x, y in zip(QI, A.column(J)))
                v = [(v[idx] - R[i][J] * QI[idx]) for idx in range(N)]

            # Normalize v to get the next column of Q and R
            norm = math.sqrt(sum(x**2 for x in v))
            R[J][J] = norm

            # Set the next column of Q to the normalized v, or zero if norm is too small
            if norm > 1e-12:
                Q.set_column(J, [x / norm for x in v])
            else:
                Q.set_column(J, [0.0] * N)

        # Return the Q and R matrices
        return Q, R

    def _eigen(self, max_iters: int = 150) -> tuple[list[float], list[Vector]]:
        n = self.shape[0]
        ak = Matrix([[self[r][c] for c in range(n)] for r in range(n)])
        i = Matrix(shape=(n, n)).to_identity

        # Iteratively apply QR decomposition to converge on eigenvalues
        for _ in range(max_iters):
            Q, R = self.__QR_decomp(ak)

            # Update Ak and i to converge on eigenvalues
            ak = R @ Q
            i = i @ Q

            # Check for convergence (off-diagonal elements should be small)
            off_diagonal_sum = 0.0
            for r in range(n):
                for c in range(n):
                    if r != c:
                        off_diagonal_sum += abs(ak[r][c])

            # If off-diagonal elements are small, we've converged
            if off_diagonal_sum < EPSILON:
                break

        # Extract eigenvalues and eigenvectors
        eigenvals = [ak[i][i] for i in range(n)]
        return eigenvals, i.to_column_vectors()

    @property
    def eigen(self) -> tuple[list[float], list[Vector]]:
        """
        Computes eigenvalues and eigenvectors using the iterative QR algorithm.

        Returns
        -------
        - `list[float]`: The eigenvalues
        - `SquareMatrix`: A matrix where columns represent the corresponding eigenvectors
        """
        if not self.is_square():
            raise ValueError(
                "Matrix must be square to compute eigenvalues and eigenvectors."
            )
        return self._eigen()

    def _diagonal(self) -> list[float]:
        return [self[idx][idx] for idx in range(self.shape[0])]

    @property
    def diagonal(self) -> list[float]:
        """Returns the diagonal of the matrix as a list."""
        if not self.is_square():
            raise ValueError("Matrix must be square to compute the diagonal.")
        return self._diagonal()

    def _trace(self) -> float:
        return math.fsum(self._diagonal())

    @property
    def trace(self) -> float:
        """
        Returns the trace of the matrix.

        The trace is defined as the sum of all the elements on the diagonal, e. g. `A_00`, `A_11`, `A_22`, etc.
        """
        if not self.is_square():
            raise ValueError("Matrix must be square to compute the trace.")
        return self._trace()

    def _to_identity(self) -> Matrix:
        """Matrix constructor that returns the identity matrix of the given size."""
        matrix = Matrix(shape=self.shape)
        for idx in range(self.shape[0]):
            matrix[idx][idx] = 1

        return matrix

    @property
    def to_identity(self) -> Matrix:
        """Returns the identity matrix of the same dimension as this matrix."""
        if not self.is_square():
            raise ValueError(
                "Matrix must be square to be converted to an identity matrix."
            )
        return self._to_identity()

    def is_singular(self) -> bool:
        """Returns if the matrix is singular, which is a matrix with a determinant of 0."""
        if not self.is_square():
            raise ValueError("Matrix must be square to be singular.")
        return self.det == 0

    def is_identity(self) -> bool:
        """Returns if the matrix is equal to the identity matrix of the same dimension."""
        if not self.is_square():
            raise ValueError("Matrix must be square to be an identity matrix.")
        return self == self.to_identity

    def is_diagonal(self) -> bool:
        if not self.is_square():
            raise ValueError("Matrix must be square to be diagonal.")

        """Returns if the matrix is diagonal.

        A diagonal matrix is a matrix where all the elements outside of the leading diagonal is 0.
        The identity matrix is a common example.
        """
        for idx1 in range(self.shape[0]):
            for idx2 in range(self.shape[1]):
                if idx1 != idx2 and self[idx1][idx2] != 0:
                    return False
                else:
                    continue
        return True

    def is_symmetric(self) -> bool:
        """Returns if the matrix is symmetric, which is a matrix that is equal to its transpose."""
        if not self.is_square():
            raise ValueError("Matrix must be square to be symmetric.")
        return self == self.T

    def is_nilpotent(self) -> bool:
        """Returns True if the matrix raised to some power becomes a zero matrix."""
        if not self.is_square():
            raise ValueError("Matrix must be square to be nilpotent.")
        return all(value == 0 for value in self.eigen[0]) and self.det == 0

    def is_idempotent(self) -> bool:
        """Returns True if the matrix multiplied by itself equals itself: `A^2` = `A`."""
        if not self.is_square():
            raise ValueError("Matrix must be square to be idempotent.")
        return self == self @ self

    def is_orthogonal(self) -> bool:
        """Returns if the matrix is orthogonal, which is a matrix whose transpose is equal to its inverse."""
        if not self.is_square():
            raise ValueError("Matrix must be square to be orthogonal.")
        return self.T == self.inverse

    def is_invertible(self) -> bool:
        """Returns if the matrix is invertible, which is a matrix whose determinant is not 0."""
        if not self.is_square():
            raise ValueError("Matrix must be square to be invertible.")
        return self.det != 0

    def is_skew_symmetric(self) -> bool:
        """
        Returns if the matrix is skew-symmetric.

        A skew-symmetric matrix is a matrix whose transpose is equal to its negative.
        """
        if not self.is_square():
            raise ValueError("Matrix must be square to be skew-symmetric.")
        return self.T == -(self)

    def is_upper_triangular(self) -> bool:
        """
        Returns if the matrix is upper triangular.

        An upper triangular matrix is a matrix whose elements below the leading diagonal are all 0.
        """
        if not self.is_square():
            raise ValueError("Matrix must be square to be upper triangular.")
        for idx1 in range(1, self.shape[0]):
            for idx2 in range(idx1):
                if self[idx1][idx2] != 0:
                    return False
        return True

    def is_lower_triangular(self) -> bool:
        """
        Returns if the matrix is lower triangular.

        An lower triangular matrix is a matrix whose elements above the leading diagonal are all 0.
        """
        if not self.is_square():
            raise ValueError("Matrix must be square to be lower triangular.")
        for idx1 in range(self.shape[0]):
            for idx2 in range(idx1 + 1, self.shape[1]):
                if self[idx1][idx2] != 0:
                    return False
        return True

    def is_positive_definite(self) -> bool:
        """
        Returns True if all eigenvalues are strictly positive.
        """
        return all(value > 0 for value in self.eigen[0])


def rot_x(θ: float) -> Matrix:
    """Returns the rotation matrix for a rotation around the x-axis by the given angle in degrees."""
    θ = math.radians(θ)
    return Matrix(
        [[1, 0, 0], [0, math.cos(θ), -math.sin(θ)], [0, math.sin(θ), math.cos(θ)]]
    )


def rot_y(θ: float) -> Matrix:
    """Returns the rotation matrix for a rotation around the y-axis by the given angle in degrees."""
    θ = math.radians(θ)
    return Matrix(
        [[math.cos(θ), 0, math.sin(θ)], [0, 1, 0], [-math.sin(θ), 0, math.cos(θ)]]
    )


def rot_z(θ: float) -> Matrix:
    """Returns the rotation matrix for a rotation around the z-axis by the given angle in degrees."""
    θ = math.radians(θ)
    return Matrix(
        [[math.cos(θ), -math.sin(θ), 0], [math.sin(θ), math.cos(θ), 0], [0, 0, 1]]
    )
