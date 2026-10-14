"""
The `DuraPy` `UniCrypto` module.

UniCrypto includes a range of cryptography methods, for both encryption and decryption.
"""

from .unicrypto import (
    binary_decode,
    binary_encode,
    ceasar_decode,
    ceasar_encode,
    otp_decrypt,
    otp_encrypt,
    railfence_decode,
    railfence_encode,
    vigenere_decode,
    vigenere_encode,
)

__all__ = [
    "binary_decode",
    "binary_encode",
    "ceasar_decode",
    "ceasar_encode",
    "otp_decrypt",
    "otp_encrypt",
    "railfence_decode",
    "railfence_encode",
    "vigenere_decode",
    "vigenere_encode",
]
