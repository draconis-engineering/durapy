"""`UniCrypto` source"""


def binary_encrypt(plaintext: str) -> str:
    """Binary encryption"""
    binary = "".join(format(ord(char), "08b") for char in plaintext)
    return " ".join(binary[i : i + 8] for i in range(0, len(binary), 8))


def binary_decrypt(binary: str) -> str:
    """Binary decryption"""
    return "".join(chr(int(b, 2)) for b in binary.split())


def ceasar_encrypt(plaintext: str, key: int) -> str:
    """Ceasar encryption"""
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


def ceasar_decrypt(cipher: str, key: int) -> str:
    """Ceasar decryption"""
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


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Vigenêre encryption"""
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


def vigenere_decrypt(cipher: str, key: str) -> str:
    """Vigenêre decryption"""
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


def railfence_encrypt(plaintext: str, key: int) -> str:
    """Railfence encryption"""
    key = int(key)
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


def railfence_decrypt(cipher: str, key: int) -> str:
    """Railfence decryption"""
    key = int(key)
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


def otp_encrypt(plaintext: str, key: str) -> str:
    """One Time Pad encryption — key must be at least as long as plaintext"""
    if len(key) < len(plaintext):
        raise ValueError("OTP key must be at least as long as plaintext")
    binary_text = "".join(format(ord(i), "08b") for i in plaintext)
    binary_key = "".join(format(ord(i), "08b") for i in key)
    # Only use key bits matching plaintext length
    binary_key = binary_key[: len(binary_text)]
    cipher = "".join(str(int(b1) ^ int(b2)) for b1, b2 in zip(binary_text, binary_key))
    return " ".join(cipher[i : i + 8] for i in range(0, len(cipher), 8))


def otp_decrypt(cipher: str, key: str) -> str:
    """One Time Pad decryption"""
    # Remove spaces from cipher
    cipher_bits = cipher.replace(" ", "")
    bintext = "".join(format(ord(i), "08b") for i in key)
    bintext = bintext[: len(cipher_bits)]
    if len(bintext) < len(cipher_bits):
        raise ValueError("Key too short for given cipher")
    plaintext_bits = "".join(
        str(int(b1) ^ int(b2)) for b1, b2 in zip(cipher_bits, bintext)
    )
    return "".join(
        chr(int(plaintext_bits[i : i + 8], 2)) for i in range(0, len(plaintext_bits), 8)
    )
