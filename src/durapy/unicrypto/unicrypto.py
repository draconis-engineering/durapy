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
    cipher = ""

    for idx, char in enumerate(plaintext):
        if char.isalpha():
            if char.isupper():
                cipher += chr(
                    (ord(char) - ord(key[idx % len(key)].upper()) + 26) % 26 + ord("A")
                )
            else:
                cipher += chr(
                    (ord(char) - ord(key[idx % len(key)].lower()) + 26) % 26 + ord("a")
                )
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
    """One Time Pad encryption"""
    binary_text = "".join(format(ord(i), "08b") for i in plaintext)
    binary_key = "".join(format(ord(i), "08b") for i in key)
    cipher = "".join(str(int(b1) ^ int(b2)) for b1, b2 in zip(binary_text, binary_key))
    return " ".join(cipher[i : i + 8] for i in range(0, len(cipher), 8))


def otp_decrypt(cipher: str, key: str) -> str:
    """One Time Pad decryption"""
    bintext = "".join(format(ord(i), "08b") for i in key)
    plaintext_bits = "".join(str(int(b1) ^ int(b2)) for b1, b2 in zip(cipher, bintext))
    return "".join(
        chr(int(plaintext_bits[i : i + 8], 2)) for i in range(0, len(plaintext_bits), 8)
    )
