"""
The `DuraPy` `UniPy` `UniCrypt` module.
This module contains all the encryption and decryption functions of the `DuraPy` library.
These include methods such as binary, ceasar, vigenere, railfence and OTP with encryption and decryption for all cryptography methods.
"""

from .unicrypt import (
    binary_decrypt,
    binary_encrypt,
    ceasar_decrypt,
    ceasar_encrypt,
    otp_decrypt,
    otp_encrypt,
    railfence_decrypt,
    railfence_encrypt,
    vigenere_decrypt,
    vigenere_encrypt,
)

__all__ = [
    "binary_decrypt",
    "binary_encrypt",
    "ceasar_decrypt",
    "ceasar_encrypt",
    "otp_decrypt",
    "otp_encrypt",
    "railfence_decrypt",
    "railfence_encrypt",
    "vigenere_decrypt",
    "vigenere_encrypt",
]
