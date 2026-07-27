
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

// Matrix-Matrix Multiplication
py::array_t<double> mat_mat_mul(py::array_t<double> a, py::array_t<double> b) {
    auto r_a = a.unchecked<2>(); // 2D accessor
    auto r_b = b.unchecked<2>(); // 2D accessor

    size_t rows_a = r_a.shape(0);
    size_t cols_a = r_a.shape(1);
    size_t cols_b = r_b.shape(1);

    // Allocate continuous output memory buffer matching NumPy layout
    py::array_t<double> result({rows_a, cols_b});
    auto r_res = result.mutable_unchecked<2>();

    // Initialize buffer to 0
    std::fill(result.mutable_data(), result.mutable_data() + result.size(), 0.0);

    for (size_t i = 0; i < rows_a; ++i) {
        for (size_t k = 0; k < cols_a; ++k) { // Re-ordered loop (i-k-j) for CPU cache friendliness
            double val_a = r_a(i, k);
            for (size_t j = 0; j < cols_b; ++j) {
                r_res(i, j) += val_a * r_b(k, j);
            }
        }
    }
    return result;
}

// Matrix-Vector Multiplication (Returns a 2D column matrix [N, 1])
py::array_t<double> mat_vec_mul(py::array_t<double> a, py::array_t<double> b) {
    auto r_a = a.unchecked<2>();
    auto r_b = b.unchecked<1>();

    size_t rows_a = r_a.shape(0);
    size_t cols_a = r_a.shape(1);

    py::array_t<double> result(static_cast<py::ssize_t>(rows_a));
    auto r_res = result.mutable_unchecked<1>();

    for (size_t i = 0; i < rows_a; ++i) {
        double sum = 0.0;
        for (size_t j = 0; j < cols_a; ++j) {
            sum += r_a(i, j) * r_b(j);
        }
        r_res(i) = sum;
    }

    return result;
}

// Vector-Matrix Multiplication (Returns a 2D column matrix [N, 1])
py::array_t<double> vec_mat_mul(py::array_t<double> a, py::array_t<double> b) {
    auto r_a = a.unchecked<1>();
    auto r_b = b.unchecked<2>();

    size_t rows_b = r_b.shape(0);
    size_t cols_b = r_b.shape(1);

    py::array_t<double> result({rows_b, size_t(1)});
    auto r_res = result.mutable_unchecked<2>();

    for (size_t i = 0; i < rows_b; ++i) {
        double sum = 0.0;
        for (size_t j = 0; j < cols_b; ++j) {
            sum += r_a(j) * r_b(i, j);
        }
        r_res(i, 0) = sum;
    }
    return result;
}

// Vector Dot Product (Returns a primitive scalar)
double dot_product(py::array_t<double> a, py::array_t<double> b) {
    auto r_a = a.unchecked<1>();
    auto r_b = b.unchecked<1>();

    double result = 0.0;
    for (size_t i = 0; i < r_a.size(); i++) {
        result += r_a(i) * r_b(i);
    }
    return result;
}

py::array_t<double> outer_product(py::array_t<double> a, py::array_t<double> b) {
    // Enforce that input arrays are 1D vectors
    if (a.ndim() != 1 || b.ndim() != 1) {
        throw std::invalid_argument("Inputs must be 1D vectors for an outer product.");
    }

    // Get read-only 1D proxies for the input vectors
    auto r_a = a.unchecked<1>();
    auto r_b = b.unchecked<1>();

    size_t size_a = r_a.shape(0);
    size_t size_b = r_b.shape(0);

    // Allocate a 2D result matrix of shape (size_a, size_b)
    py::array_t<double> result({size_a, size_b});

    // Get a mutable 2D proxy to write the results
    auto r_res = result.mutable_unchecked<2>();

    // Compute the outer product: A[i, j] = a[i] * b[j]
    for (size_t i = 0; i < size_a; ++i) {
        double val_a = r_a(i); // Cache to avoid redundant lookups
        for (size_t j = 0; j < size_b; ++j) {
            r_res(i, j) = val_a * r_b(j);
        }
    }

    return result;
}

// Register the module
PYBIND11_MODULE(_maxcompute, m) {
    m.doc() = "MX | MaxCompute C++ Accelerated Computation Platform";

    // call_guard releases the GIL so these math operations can scale up multi-threaded Python apps
    m.def("mat_mat_mul", &mat_mat_mul, "Matrix-Matrix multiplication");
    m.def("mat_vec_mul", &mat_vec_mul, "Matrix-Vector multiplication");
    m.def("vec_mat_mul", &vec_mat_mul, "Vector-Matrix multiplication");
    m.def("dot_product", &dot_product, "Vector-dot product");
    m.def("outer_product", &outer_product, "Vector-outer product");
}
