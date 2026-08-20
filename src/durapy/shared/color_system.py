"""
The `DuraPy` Color System module.

This module includes terminal text coloring tools and color data classes such as `RGB`, `HEX` and `CMYK`.
"""

from __future__ import annotations

from typing import overload

ANSI_COLORS: dict[str, str] = {
    "black": "\033[30m",
    "brown": "\033[38;5;94m",
    "red": "\033[31m",
    "crimson": "\033[38;5;161m",
    "orange": "\033[38;5;208m",
    "yellow": "\033[33m",
    "green": "\033[32m",
    "cyan": "\033[36m",
    "blue": "\033[34m",
    "navy": "\033[38;5;17m",
    "light blue": "\033[38;5;117m",
    "pastel blue": "\033[38;5;153m",
    "violet": "\033[38;5;93m",
    "magenta": "\033[35m",
    "pink": "\033[38;5;205m",
    "light gray": "\033[37m",
    "gray": "\033[90m",
    "dark gray": "\033[38;5;240m",
    "white": "\033[97m",
    "gold": "\033[38;5;178m",
    "silver": "\033[38;5;246m",
    "teal": "\033[38;5;30m",
    "lime": "\033[38;5;154m",
}


def color_text(
    text: object,
    color: str | None,
    bold: bool = False,
    underline: bool = False,
    italic: bool = False,
) -> str:
    """Returns the given text in the given color using `ANSI` escape codes. If the color is not found, it returns the text without coloring."""

    if color is None or color.lower() not in ANSI_COLORS:
        return str(text)

    text = str(text)
    ansi = ANSI_COLORS.get(color.lower(), "\033[0m")

    if bold:
        ansi += "\033[1m"
    if underline:
        ansi += "\033[4m"
    if italic:
        ansi += "\033[3m"
    return ansi + text + "\033[0m"


def clip_int(val: int, lower: int, upper: int) -> int:
    """Clips the given integer to the given range."""
    if val <= lower:
        return lower
    elif val >= upper:
        return upper
    return val


def validate_hex(hexcode: str) -> str:
    """Validates a hexstring for colors. If invalid, returns `#000000`"""
    hexcode = hexcode[1:7]
    hexchars = "abcdef0123456789"
    if len(hexcode) != 6:
        return "#000000"

    for char in hexcode.lower():
        if char not in hexchars:
            return "#000000"

    return "#" + hexcode


class _BaseColor:
    "Base class for color data types."

    def __init__(self, colorname: str) -> None:
        self.colorname: str = colorname

    def __str__(self) -> str:
        return self.colorname

    def __repr__(self) -> str:
        return self.colorname

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _BaseColor):
            return self.colorname == other.colorname
        return False

    def __hash__(self) -> int:
        return hash(self.colorname)


class RGB(_BaseColor):
    "RGB color data type."

    def __init__(self, colorname: str, r: int, g: int, b: int) -> None:
        super().__init__(colorname)
        self._r = r
        self._g = g
        self._b = b

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RGB):
            return (self.r, self.g, self.b) == (other.r, other.g, other.b)
        elif isinstance(other, HEX):
            return self.toHex().hexcode == other.hexcode
        elif isinstance(other, CMYK):
            return self.toCMYK().values == other.values
        else:
            return False

    @overload
    def __getitem__(self, key: None) -> tuple[int, int, int]: ...
    @overload
    def __getitem__(self, key: int) -> int: ...
    def __getitem__(self, key: int | None) -> int | tuple[int, int, int]:
        if key is None:
            return (self.r, self.g, self.b)
        if key in [0, 1, 2]:
            return (self.r, self.g, self.b)[key]
        raise IndexError("Key must be None or an integer in [0, 1, 2]")

    @property
    def r(self) -> int:
        """Getter: Returns the red value."""
        return self._r

    @r.setter
    def r(self, new_value: int) -> None:
        """Setter: Clips and assigns the new red value."""
        self._r = clip_int(new_value, 0, 255)

    @property
    def g(self) -> int:
        """Getter: Returns the green value."""
        return self._g

    @g.setter
    def g(self, new_value: int) -> None:
        """Setter: Clips and assigns the new green value."""
        self._g = clip_int(new_value, 0, 255)

    @property
    def b(self) -> int:
        """Getter: Returns the blue value."""
        return self._b

    @b.setter
    def b(self, new_value: int) -> None:
        """Setter: Clips and assigns the new blue value."""
        self._b = clip_int(new_value, 0, 255)

    def toHex(self) -> HEX:
        """Converts the RGB color to a hexadecimal color code in the format "#RRGGBB"."""
        return HEX(self.colorname, f"#{self.r:02x}{self.g:02x}{self.b:02x}")

    def toCMYK(self) -> CMYK:
        """Converts the RGB color to CMYK color values."""
        r_scaled = self.r / 255
        g_scaled = self.g / 255
        b_scaled = self.b / 255

        k = 1 - max(r_scaled, g_scaled, b_scaled)
        if k == 1:
            return CMYK(self.colorname, 0, 0, 0, 100)

        c = (1 - r_scaled - k) / (1 - k)
        m = (1 - g_scaled - k) / (1 - k)
        y = (1 - b_scaled - k) / (1 - k)

        return CMYK(
            self.colorname, int(c * 100), int(m * 100), int(y * 100), int(k * 100)
        )


class HEX(_BaseColor):
    "Hex color data type."

    def __init__(self, colorname: str, hexcode: str):
        super().__init__(colorname)
        self.hexcode = validate_hex(hexcode)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HEX):
            return self.hexcode == other.hexcode
        elif isinstance(other, RGB):
            return self.toRGB() == other
        elif isinstance(other, CMYK):
            return self.toCMYK().values == other.values
        else:
            return False

    @property
    def r(self) -> int:
        """Getter: Returns the red value as an integer (0-255)."""
        return int(self.hexcode[1:3], 16)

    @r.setter
    def r(self, new_hex: str) -> None:
        """Setter: Updates the red component in the hex string."""
        self.hexcode = validate_hex("#" + new_hex + self.hexcode[3:])

    @property
    def g(self) -> int:
        """Getter: Returns the green value as an integer (0-255)."""
        return int(self.hexcode[3:5], 16)

    @g.setter
    def g(self, new_hex: str) -> None:
        """Setter: Updates the green component in the hex string."""
        self.hexcode = validate_hex(self.hexcode[:3] + new_hex + self.hexcode[5:])

    @property
    def b(self) -> int:
        """Getter: Returns the blue value as an integer (0-255)."""
        return int(self.hexcode[5:7], 16)

    @b.setter
    def b(self, new_hex: str) -> None:
        """Setter: Updates the blue component in the hex string."""
        self.hexcode = validate_hex(self.hexcode[:5] + new_hex)

    def toRGB(self) -> RGB:
        """Converts the hexadecimal color code to RGB color values."""
        hexcode = self.hexcode.lstrip("#")
        r = int(hexcode[0:2], 16)
        g = int(hexcode[2:4], 16)
        b = int(hexcode[4:6], 16)
        return RGB(self.colorname, r, g, b)

    def toCMYK(self) -> CMYK:
        """Converts the hexadecimal color code to CMYK color values."""
        rgb = self.toRGB()
        r_scaled = rgb.r / 255
        g_scaled = rgb.g / 255
        b_scaled = rgb.b / 255

        k = 1 - max(r_scaled, g_scaled, b_scaled)
        if k == 1:
            return CMYK(self.colorname, 0, 0, 0, 100)  # Pure black

        c = (1 - r_scaled - k) / (1 - k)
        m = (1 - g_scaled - k) / (1 - k)
        y = (1 - b_scaled - k) / (1 - k)

        return CMYK(
            self.colorname, int(c * 100), int(m * 100), int(y * 100), int(k * 100)
        )


class CMYK(_BaseColor):
    "CMYK color data type."

    def __init__(self, colorname: str, c: int, m: int, y: int, k: int):
        super().__init__(colorname)
        self.c: int = clip_int(c, 0, 100)
        self.m: int = clip_int(m, 0, 100)
        self.y: int = clip_int(y, 0, 100)
        self.k: int = clip_int(k, 0, 100)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CMYK):
            return (self.c, self.m, self.y, self.k) == (
                other.c,
                other.m,
                other.y,
                other.k,
            )
        elif isinstance(other, RGB):
            return self.toRGB() == other
        elif isinstance(other, HEX):
            return self.toHex() == other
        else:
            return False

    @property
    def values(self) -> tuple[int, int, int, int]:
        return (self.c, self.m, self.y, self.k)

    def toRGB(self) -> RGB:
        """Converts the CMYK color values to RGB color values."""
        r = 255 * (1 - self.c / 100) * (1 - self.k / 100)
        g = 255 * (1 - self.m / 100) * (1 - self.k / 100)
        b = 255 * (1 - self.y / 100) * (1 - self.k / 100)
        return RGB(self.colorname, int(r), int(g), int(b))

    def toHex(self) -> HEX:
        """Converts the CMYK color values to a hexadecimal color code in the format "#RRGGBB"."""
        r, g, b = self.toRGB()
        return HEX(self.colorname, f"#{r:02x}{g:02x}{b:02x}")
