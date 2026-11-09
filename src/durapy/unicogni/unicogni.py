"""`UniCogni` source"""

import math

import dracolix as dlx
import numpy as np
from scipy import special

from ..shared.constants import PI

### NOTE:
# Still heavily dependent on NumPy.
# Replace all numpy functionality and remove as dep when dracolix version is >= 0.4.x

# -------------------------------------- #
#          ACTIVATION FUNCTIONS          #
# -------------------------------------- #


def relu(x: np.ndarray, /) -> dlx.Array:
    """Returns the Rectified Linear Unit activation of x."""
    return dlx.array(np.maximum(0.0, x))


def d_relu(x: dlx.Array, /) -> dlx.Array:
    """Returns the derivative of the Rectified Linear Unit activation function."""
    return (x > 0).astype(dlx.f32)


def leaky_relu(x: np.ndarray, /) -> dlx.Array:
    """Returns the Leaky ReLU activation of X."""
    return dlx.array(np.maximum(0.01 * x, x))


def d_leaky_relu(x: np.ndarray, /) -> dlx.Array:
    """Returns the derivative of the Leaky ReLU activation function."""
    return dlx.array(np.where(x > 0, 1.0, 0.01).astype(np.float32))


def gelu(x: dlx.Array, /) -> dlx.Array:
    """Gaussian Error Linear Unit using the tanh approximation."""
    return 0.5 * x * (1.0 + tanh(math.sqrt(2.0 / PI.value) * (x + 0.044715 * x**3)))


def d_gelu(x: np.ndarray, /) -> np.ndarray:
    """Derivative of GELU."""
    try:
        gauss = np.exp(-0.5 * x**2)
    except OverflowError:
        gauss = 0.0
    cdf = 0.5 * (1.0 + special.erf(x / math.sqrt(2)))
    pdf = (1.0 / math.sqrt(2 * PI.value)) * gauss
    return cdf + x * pdf


def silu(x: dlx.Array, /) -> dlx.Array:
    """Sigmoid Linear Unit."""
    return x * sigmoid(x)


def d_silu(x: dlx.Array, /) -> dlx.Array:
    """Derivative of the SiLU activation function."""
    s = sigmoid(x)
    return s * (1.0 + x * (1.0 - s))


def prelu(x: np.ndarray, /, *, a: float) -> np.ndarray:
    """Parametric ReLU."""
    return np.maximum(0.0, x) + a * np.minimum(0.0, x)


def dx_prelu(x: np.ndarray, /, *, a: float) -> np.ndarray:
    """Derivative of PReLU with respect to x. Note: you will also need a gradient w.r.t 'a' during backprop!"""
    return np.where(x > 0, 1.0, a)


# dxprelu needs gradient w.r.t. A


def da_prelu(x: np.ndarray, /, *, a: float) -> np.ndarray:
    """Derivative of PReLU with respect to 'a'."""
    return np.where(x < 0, x, 0.0)


def cdelu(x: np.ndarray, /, *, a: float = 1.0) -> np.ndarray:
    """Continuously Differentiable Exponential Linear Unit (CDELU)."""
    return np.maximum(0.0, x) + np.minimum(0.0, a * np.expm1(x / a))


def d_cdelu(x: np.ndarray, /, *, a: float = 1.0) -> np.ndarray:
    """Derivative of the CDELU activation function."""
    return np.where(x > 0, 1.0, np.exp(x / a))


def sigmoid(x: dlx.Array, /) -> dlx.Array:
    """Returns the Sigmoid activation of x with overflow protection."""
    expx = np.array(dlx.exp(x))
    npx = np.array(x)
    return dlx.array(
        np.where(npx >= 0, 1.0 / (1.0 + np.exp(-npx)), expx / (1.0 + expx))
    )


def d_sigmoid(x: dlx.Array, /) -> dlx.Array:
    """Returns the derivative of the Sigmoid activation function."""
    s = sigmoid(x)
    return s * (1.0 - s)


def tanh(x: dlx.Array, /) -> dlx.Array:
    """Returns the Tanh activation of x using a numerically stable approach."""
    return dlx.tanh(x)


def d_tanh(x: dlx.Array, /) -> dlx.Array:
    """Returns the derivative of the Tanh activation function."""
    t = tanh(x)
    return 1.0 - t**2


def swish(x: dlx.Array, /, *, β: float = 1.0) -> dlx.Array:
    """Swish activation function."""
    return x * sigmoid(x * β)


def d_swish(x: dlx.Array, /, *, β: float = 1.0) -> dlx.Array:
    """Derivative of the Swish activation function."""
    s = sigmoid(x * β)
    return s + (β * x * s * (1.0 - s))


def mish(x: np.ndarray, /) -> dlx.Array:
    """A self-regularized, smooth, non-monotonic activation function."""
    softplus = np.where(x < 20.0, np.log1p(np.exp(x)), x)
    return x * tanh(dlx.array(softplus))


def d_mish(x: np.ndarray, /) -> np.ndarray:
    """Derivative of the Mish activation function."""

    # Clip the exponent so exp(x) cannot overflow to inf (which yields nan,
    # since np.exp on an array warns instead of raising OverflowError).
    # For x > 20 the derivative is already 1 to within float precision.
    ex = np.exp(np.minimum(x, 20.0))

    omega = 4.0 * (x + 1.0) + 4.0 * ex**2 + ex**3 + ex * (4.0 * x + 6.0)
    delta = 2.0 * ex + ex**2 + 2.0
    return (ex * omega) / (delta**2)


def softmax(z: np.ndarray, /) -> np.ndarray:
    """Softmax activation function for multi-class classification. Converts raw scores (logits) into probabilities."""
    exp_z = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=-1, keepdims=True)


# ------------------------------------- #
#          PERFORMANCE METRICS          #
# ------------------------------------- #


def mae(actual: dlx.Array, pred: dlx.Array) -> float:
    """Mean Absolute Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")

    return float(dlx.abs(dlx.asarray(actual) - dlx.asarray(pred)).mean().real)


def mse(actual: dlx.Array, pred: dlx.Array) -> float:
    """Mean Squared Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")

    return float(((dlx.asarray(actual) - dlx.asarray(pred)) ** 2).mean().real)


def mse_grad(actual: dlx.Array, pred: dlx.Array) -> dlx.Array:
    """Gradient of the Mean Squared Error metric function (d/d_pred MSE)"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")

    return 2 * (dlx.asarray(pred) - dlx.asarray(actual)) / len(dlx.asarray(actual))


def rmse(actual: dlx.Array, pred: dlx.Array) -> float:
    """Root Mean Squared Error metric function"""
    if len(pred) != len(actual):
        raise ValueError("Loss functions must be given two equal-length arrays/lists!")

    return math.sqrt(mse(actual, pred))


def cross_entropy_loss(actual: np.ndarray, pred: np.ndarray) -> float:
    """Cross-entropy loss function for multi-class classification.

    ``pred`` holds raw logits and is normalized with a numerically stable
    softmax over the last axis. ``actual`` is treated as one-hot (or
    probability) targets and the class index is taken via ``argmax`` along the
    same axis. Works for both 1-D (a single sample) and N-D inputs.
    """
    actual = np.asarray(actual, dtype=np.float64)
    pred = np.asarray(pred, dtype=np.float64)

    if actual.shape != pred.shape:
        raise ValueError(
            "Loss functions must be given two equal-shape arrays! "
            f"Got {actual.shape} and {pred.shape}"
        )
    if actual.ndim == 0:
        raise ValueError("Cross-entropy loss requires at least a 1-D input.")

    probabilities = np.clip(softmax(pred), 1e-15, 1.0)
    targets = np.argmax(actual, axis=-1)

    if pred.ndim == 1:
        return float(-np.log(probabilities[targets]))

    # Flatten all leading (sample) dimensions and gather the target class.
    flat_probabilities = probabilities.reshape(-1, probabilities.shape[-1])
    flat_targets = targets.reshape(-1)
    log_likelihood = -np.log(
        flat_probabilities[np.arange(flat_probabilities.shape[0]), flat_targets]
    )

    return float(np.mean(log_likelihood))
