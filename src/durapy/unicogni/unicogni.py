"""`UniCogni` source"""

import numpy as np
from scipy import special

from ..shared.constants import PI

### ACTIVATION FUNCTIONS


def relu(x: np.ndarray) -> np.ndarray:
    """Returns the Rectified Linear Unit activation of x."""
    return np.maximum(0.0, x)


def d_relu(x: np.ndarray) -> np.ndarray:
    """Returns the derivative of the Rectified Linear Unit activation function."""
    return (x > 0).astype(np.float32)


def leaky_relu(x: np.ndarray) -> np.ndarray:
    """Returns the Leaky ReLU activation of X."""
    return np.maximum(0.01 * x, x)


def d_leaky_relu(x: np.ndarray) -> np.ndarray:
    """Returns the derivative of the Leaky ReLU activation function."""
    return np.where(x > 0, 1.0, 0.01).astype(np.float32)


def gelu(x: np.ndarray) -> np.ndarray:
    """Gaussian Error Linear Unit using the tanh approximation."""
    return 0.5 * x * (1.0 + tanh(np.sqrt(2.0 / PI.value) * (x + 0.044715 * x**3)))


def d_gelu(x: np.ndarray) -> np.ndarray:
    """Derivative of GELU."""
    try:
        gauss = np.exp(-0.5 * x**2)
    except OverflowError:
        gauss = 0.0
    cdf = 0.5 * (1.0 + special.erf(x / np.sqrt(2)))
    pdf = (1.0 / np.sqrt(2 * PI.value)) * gauss
    return cdf + x * pdf


def silu(x: np.ndarray) -> np.ndarray:
    """Sigmoid Linear Unit."""
    return x * sigmoid(x)


def d_silu(x: np.ndarray) -> np.ndarray:
    """Derivative of the SiLU activation function."""
    s = sigmoid(x)
    return s * (1.0 + x * (1.0 - s))


def prelu(x: np.ndarray, a: float) -> np.ndarray:
    """Parametric ReLU."""
    return np.maximum(0.0, x) + a * np.minimum(0.0, x)


def dx_prelu(x: np.ndarray, a: float) -> np.ndarray:
    """Derivative of PReLU with respect to x. Note: you will also need a gradient w.r.t 'a' during backprop!"""
    return np.where(x > 0, 1.0, a)


def da_prelu(x: np.ndarray, a: float) -> np.ndarray:
    """Derivative of PReLU with respect to 'a'."""
    return np.where(x < 0, x, 0.0)


def cdelu(x: np.ndarray, alpha: float = 1.0) -> np.ndarray:
    """Continuously Differentiable Exponential Linear Unit (CDELU)."""
    return np.maximum(0.0, x) + np.minimum(0.0, alpha * np.expm1(x / alpha))


def d_cdelu(x: np.ndarray, alpha: float = 1.0) -> np.ndarray:
    """Derivative of the CDELU activation function."""
    return np.where(x > 0, 1.0, np.exp(x / alpha))


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Returns the Sigmoid activation of x with overflow protection."""
    expx = np.exp(x)
    return np.where(x >= 0, 1.0 / (1.0 + np.exp(-x)), expx / (1.0 + expx))


def d_sigmoid(x: np.ndarray) -> np.ndarray:
    """Returns the derivative of the Sigmoid activation function."""
    s = sigmoid(x)
    return s * (1.0 - s)


def tanh(x: np.ndarray) -> np.ndarray:
    """Returns the Tanh activation of x using a numerically stable approach."""
    return np.tanh(x)


def d_tanh(x: np.ndarray) -> np.ndarray:
    """Returns the derivative of the Tanh activation function."""
    t = tanh(x)
    return 1.0 - t**2


def swish(x: np.ndarray, β: float = 1.0) -> np.ndarray:
    """Swish activation function."""
    return x * sigmoid(x * β)


def d_swish(x: np.ndarray, β: float = 1.0) -> np.ndarray:
    """Derivative of the Swish activation function."""
    s = sigmoid(x * β)
    return s + (β * x * s * (1.0 - s))


def mish(x: np.ndarray) -> np.ndarray:
    """A self-regularized, smooth, non-monotonic activation function."""
    softplus = np.where(x < 20.0, np.log1p(np.exp(x)), x)
    return x * tanh(softplus)


def d_mish(x: np.ndarray) -> np.ndarray:
    """Derivative of the Mish activation function."""
    try:
        ex = np.exp(x)
    except OverflowError:
        return np.ones_like(x)  # Becomes linear at large positive values

    omega = 4.0 * (x + 1.0) + 4.0 * ex**2 + ex**3 + ex * (4.0 * x + 6.0)
    delta = 2.0 * ex + ex**2 + 2.0
    return (ex * omega) / (delta**2)


def softmax(Z: np.ndarray) -> np.ndarray:
    """Softmax activation function for multi-class classification. Converts raw scores (logits) into probabilities."""
    exp_z = np.exp(Z - np.max(Z, axis=-1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=-1, keepdims=True)


### PERFORMANCE METRICS


def mae(actual: np.ndarray, pred: np.ndarray) -> float:
    """Mean Absolute Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")

    return sum(np.abs(actual - pred)) / len(actual)


def mse(actual: np.ndarray, pred: np.ndarray) -> float:
    """Mean Squared Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")

    return np.mean((actual - pred) ** 2) / len(actual)


def mse_grad(actual: np.ndarray, pred: np.ndarray) -> np.ndarray:
    """Gradient of the Mean Squared Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")

    return 2 * (pred - actual) / len(actual)


def rmse(actual: np.ndarray, pred: np.ndarray) -> float:
    """Root Mean Squared Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")

    return np.sqrt(mse(actual, pred))


def cross_entropy_loss(actual: np.ndarray, pred: np.ndarray) -> float:
    """Cross-entropy loss function for multi-class classification."""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")

    array_len = actual.shape[0]
    clipped_pred = np.clip(softmax(pred), 1e-15, 1 - 1e-15)
    log_likelihood = -(np.log(clipped_pred[range(array_len), actual.argmax(axis=1)]))
    return np.sum(log_likelihood) / array_len
