"""
The `DuraPy` `UniCrypto` module.

UniCrypto includes a range of cryptography methods, for both encryption and decryption.
"""

from .unicrypto import (
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
