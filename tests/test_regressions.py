"""Regression tests for previously reported bugs.

Each test corresponds to a confirmed defect so it cannot silently return.
"""

import math

import numpy as np
import pytest

from durapy.shared.exceptions import UnitError
from durapy.shared.numval_types import Quantity
from durapy.shared.units import DEGREE, METER, RADIAN, SECOND
from durapy.unicogni.unicogni import cross_entropy_loss, d_mish, mish
from durapy.unicrypto.unicrypto import (
    binary_decrypt,
    binary_encrypt,
    otp_decrypt,
    otp_encrypt,
    vigenere_decrypt,
    vigenere_encrypt,
)
from durapy.unimath.linalg import Matrix


# --------------------------------------------------------------------------- #
# Matrix scalar operations must accept ints (not only floats)
# --------------------------------------------------------------------------- #


def test_matrix_scalar_ops_accept_ints():
    matrix = Matrix([[1, 2], [3, 4]])
    assert (matrix * 2).array == [[2, 4], [6, 8]]
    assert (2 * matrix).array == [[2, 4], [6, 8]]
    assert (matrix + 1).array == [[2, 3], [4, 5]]
    assert (1 + matrix).array == [[2, 3], [4, 5]]
    assert (matrix - 1).array == [[0, 1], [2, 3]]
    assert (matrix / 2).array == [[0.5, 1.0], [1.5, 2.0]]


def test_matrix_scalar_ops_still_accept_floats():
    matrix = Matrix([[1, 2], [3, 4]])
    assert (matrix * 2.0).array == [[2.0, 4.0], [6.0, 8.0]]
    assert (matrix + 0.5).array == [[1.5, 2.5], [3.5, 4.5]]


# --------------------------------------------------------------------------- #
# Cross-entropy must work on 1-D input and be numerically stable
# --------------------------------------------------------------------------- #


def test_cross_entropy_1d_input():
    # Perfectly confident correct class -> near-zero loss.
    loss = cross_entropy_loss(np.array([1.0, 0.0, 0.0]), np.array([10.0, 0.0, 0.0]))
    assert loss == pytest.approx(0.0, abs=1e-4)


def test_cross_entropy_uniform_matches_log_classes():
    loss = cross_entropy_loss(np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]))
    assert loss == pytest.approx(math.log(3), rel=1e-9)


def test_cross_entropy_2d_batch():
    actual = np.array([[1, 0, 0], [0, 1, 0]])
    pred = np.array([[10.0, 0.0, 0.0], [0.0, 10.0, 0.0]])
    assert cross_entropy_loss(actual, pred) < 1e-3


def test_cross_entropy_shape_mismatch_raises():
    with pytest.raises(ValueError):
        cross_entropy_loss(np.array([1.0, 0.0]), np.array([1.0, 0.0, 0.0]))


# --------------------------------------------------------------------------- #
# Binary and OTP encoding must round-trip arbitrary Unicode
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("text", ["", "Hi", "café ☕", "日本語", "emoji 😀🎉"])
def test_binary_round_trip_unicode(text):
    assert binary_decrypt(binary_encrypt(text)) == text


def test_binary_decrypt_rejects_garbage():
    with pytest.raises(ValueError):
        binary_decrypt("2 3 4")
    with pytest.raises(ValueError):
        binary_decrypt("111111111")  # 9 bits -> out of byte range


@pytest.mark.parametrize("text", ["", "Attack at dawn", "café ☕", "emoji 😀"])
def test_otp_round_trip_unicode(text):
    key = "k" * (len(text.encode("utf-8")) + 8)
    assert otp_decrypt(otp_encrypt(text, key), key) == text


def test_otp_short_key_raises():
    with pytest.raises(ValueError):
        otp_encrypt("hello", "ab")


# --------------------------------------------------------------------------- #
# Vigenère decryption must validate the key like encryption does
# --------------------------------------------------------------------------- #


def test_vigenere_empty_key_raises():
    with pytest.raises(ValueError):
        vigenere_decrypt("abc", "")
    with pytest.raises(ValueError):
        vigenere_decrypt("abc", "123")


def test_vigenere_round_trip():
    message = "Hello, World!"
    assert vigenere_decrypt(vigenere_encrypt(message, "Key"), "Key") == message


# --------------------------------------------------------------------------- #
# Unit scale must be honoured: conversion, arithmetic, and comparisons
# --------------------------------------------------------------------------- #


def test_quantity_conversion_uses_scale():
    assert Quantity(180, DEGREE).to(RADIAN).value == pytest.approx(math.pi, rel=1e-6)
    assert Quantity(math.pi, RADIAN).to(DEGREE).value == pytest.approx(180.0, rel=1e-6)


def test_quantity_addition_across_compatible_units():
    total = Quantity(180, DEGREE) + Quantity(math.pi, RADIAN)
    assert total.value == pytest.approx(360.0, rel=1e-6)

    difference = Quantity(180, DEGREE) - Quantity(math.pi, RADIAN)
    assert difference.value == pytest.approx(0.0, abs=1e-6)


def test_quantity_comparison_across_compatible_units():
    assert Quantity(180, DEGREE) > Quantity(1, RADIAN)
    assert Quantity(1, RADIAN) < Quantity(180, DEGREE)


def test_quantity_incompatible_units_raise():
    with pytest.raises(UnitError):
        Quantity(1, METER) + Quantity(1, SECOND)
    with pytest.raises(UnitError):
        Quantity(1, METER).to(SECOND)
    with pytest.raises(UnitError):
        Quantity(1, METER) < Quantity(1, SECOND)


# --------------------------------------------------------------------------- #
# d_mish is correct: it must match the numerical derivative
# (the negative dip for x < -1 is real because Mish is non-monotonic)
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("x", [-5.0, -2.0, -1.0, 0.0, 1.0, 3.0])
def test_d_mish_matches_numeric_derivative(x):
    h = 1e-6
    numeric = (
        float(mish(np.array([x + h]))[0]) - float(mish(np.array([x - h]))[0])
    ) / (2 * h)
    assert float(d_mish(np.array([x]))[0]) == pytest.approx(numeric, abs=1e-3)
