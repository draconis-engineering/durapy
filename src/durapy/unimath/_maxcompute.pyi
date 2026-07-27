"""MX | MaxCompute C++ Accelerated Computation Platform"""

from typing import TypeAlias

import numpy as np
import numpy.typing as npt

NDArray: TypeAlias = npt.NDArray[np.float64]

def mat_mat_mul(a: NDArray, b: NDArray) -> NDArray:
    """Matrix-Matrix multiplication accelerated natively in C++.

    Expects two 2D NumPy arrays of float64.
    """

def mat_vec_mul(a: NDArray, b: NDArray) -> NDArray:
    """Matrix-Vector multiplication accelerated natively in C++.

    Expects a 2D matrix array and a 1D vector array.
    """

def vec_mat_mul(a: NDArray, b: NDArray) -> NDArray:
    """Vector-Matrix multiplication accelerated natively in C++.

    Expects a 1D vector array and a 2D matrix array.
    """

def dot_product(a: NDArray, b: NDArray) -> float:
    """Vector-dot product accelerated natively in C++.

    Expects two 1D vector arrays and returns a scalar float.
    """

def outer_product(a: NDArray, b: NDArray) -> NDArray:
    """Vector-outer product accelerated natively in C++.

    Expects two 1D vector arrays and returns a 2D matrix array.
    """
