"""`UniCrypto` source"""


# ====================================== #
# -------- Encode/Decode Utils --------- #
# ====================================== #


def binary_encode(plaintext: str) -> str:
    """Encode text as space-separated 8-bit binary bytes using UTF-8.

    This is a reversible encoding, not encryption. Any Unicode input (including
    characters outside the ASCII range) round-trips correctly through
    :func:`binary_decrypt`.
    """
    data = plaintext.encode()
    return " ".join(format(byte, "08b") for byte in data)


def binary_decode(binary: str, *, is_space_separated: bool = True) -> str:
    """Decode space-separated 8-bit binary bytes back to text using UTF-8."""
    if not is_space_separated:
        binary = " ".join(binary[i : i + 8] for i in range(0, len(binary), 8))
    try:
        data = bytes(int(chunk, 2) for chunk in binary.split())
    except ValueError as exc:
        raise ValueError(f"Invalid binary input: {exc}") from exc
    return data.decode()


def ceasar_encode(plaintext: str, key: int) -> str:
    """Ceasar cipher encoding"""

    # Explicitly deny bool key (subclass of integer)
    if not isinstance(key, int) or isinstance(key, bool):
        raise TypeError("Railfence key must be an integer")

    cipher = ""
    for char in plaintext:
        if char.isalpha():
            pos = ord(char.lower()) - 96
            new_pos = (pos + key - 1) % 26 + 1
            new_char = chr(new_pos + 96)
            cipher += new_char
        else:
            cipher += char
    return cipher


def ceasar_decode(cipher: str, key: int) -> str:
    """Ceasar cipher decoding"""

    # Explicitly deny bool key (subclass of integer)
    if not isinstance(key, int) or isinstance(key, bool):
        raise TypeError("Railfence key must be an integer")

    plaintext = ""
    for char in cipher:
        if char.isalpha():
            pos = ord(char.lower()) - 96
            new_pos = (pos - key - 1) % 26 + 1
            new_char = chr(new_pos + 96)
            plaintext += new_char
        else:
            plaintext += char
    return plaintext


def vigenere_encode(plaintext: str, key: str) -> str:
    """Vigenêre encoding"""
    if not key or not key.isalpha():
        raise ValueError("Key must be non-empty alphabetic string")
    cipher = ""
    key_idx = 0
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)].lower()) - ord("a")
            base = ord("A") if char.isupper() else ord("a")
            cipher += chr((ord(char) - base + shift) % 26 + base)
            key_idx += 1
        else:
            cipher += char
    return cipher


def vigenere_decode(cipher: str, key: str) -> str:
    """Vigenêre cipher decoding"""

    if not key or not key.isalpha():
        raise ValueError("Key must be non-empty alphabetic string")

    plaintext = ""
    key = key.lower()
    key_idx = 0

    for char in cipher:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord("a")
            if char.isupper():
                decrypted_char = chr(
                    (ord(char) - ord("A") - shift + 26) % 26 + ord("A")
                )
            else:
                decrypted_char = chr(
                    (ord(char) - ord("a") - shift + 26) % 26 + ord("a")
                )
            plaintext += decrypted_char
            key_idx += 1
        else:
            plaintext += char

    return plaintext


def railfence_encode(plaintext: str, key: int) -> str:
    """Railfence cipher encoding"""

    # Explicitly deny bool key (subclass of integer)
    if not isinstance(key, int) or isinstance(key, bool):
        raise TypeError("Railfence key must be an integer")

    if key <= 1:
        raise ValueError("Railfence key must be >= 2")

    if key > len(plaintext):
        return plaintext

    pos, direction = 0, 1
    rows: list[list[str]] = [[] for _ in range(key)]

    for char in plaintext:
        rows[pos].append(char)

        pos += direction
        if pos == 0 or pos == key - 1:
            direction *= -1

    return "".join(["".join(row) for row in rows])


def railfence_decode(cipher: str, key: int) -> str:
    """Railfence cipher decoding"""

    # Explicitly deny bool key (subclass of integer)
    if not isinstance(key, int) or isinstance(key, bool):
        raise TypeError("Railfence key must be an integer")

    if key <= 1:
        raise ValueError("Railfence key must be >= 2")

    if key > len(cipher):
        return cipher

    pattern: list[int] = []
    rows: list[list[str]] = []
    pos, idx, direction = 0, 0, 1
    plaintext = ""

    for _ in range(len(cipher)):
        pattern.append(pos)
        pos += direction
        if pos == 0 or pos == key - 1:
            direction *= -1

    counts = [pattern.count(r) for r in range(key)]

    for c in counts:
        rows.append(list(cipher[idx : idx + c]))
        idx += c

    row_ptrs = [0] * key

    for r in pattern:
        plaintext += rows[r][row_ptrs[r]]
        row_ptrs[r] += 1

    return plaintext


# ====================================== #
# -------- Encrypt/Decrypt Utils ------- #
# ====================================== #


def otp_encrypt(plaintext: str, key: str) -> str:
    """One Time Pad encryption.

    The key must be at least as long as the UTF-8 encoding of the plaintext.
    The output is space-separated 8-bit binary of the XOR stream.

    Note that this is only information-theoretically secure when the key is truly random, used once, and kept secret.
    """
    text = plaintext.encode()
    key_bytes = key.encode()
    if len(key_bytes) < len(text):
        raise ValueError("OTP key must be at least as long as plaintext")
    cipher = bytes(t ^ k for t, k in zip(text, key_bytes))
    return " ".join(format(byte, "08b") for byte in cipher)


def otp_decrypt(cipher: str, key: str) -> str:
    """One Time Pad decryption (inverse of :func:`otp_encrypt`)."""
    key_bytes = key.encode()
    try:
        cipher_bytes = bytes(int(chunk, 2) for chunk in cipher.split())
    except ValueError as exc:
        raise ValueError(f"Invalid cipher input: {exc}") from exc
    if len(key_bytes) < len(cipher_bytes):
        raise ValueError("Key too short for given cipher")
    plain = bytes(c ^ k for c, k in zip(cipher_bytes, key_bytes))
    return plain.decode()
