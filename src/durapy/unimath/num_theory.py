"""`UniMath` Number Theory source"""

import math

__all__ = [
    "factorial",
    "fibonacci_integer",
    "fibonacci_list",
    "gcd",
    "is_abundant_number",
    "is_amicable_pair",
    "is_deficient_number",
    "is_perfect_cube",
    "is_perfect_number",
    "is_perfect_power",
    "is_perfect_square",
    "is_prime",
    "is_sociable_chain",
    "lcm",
    "lovelace",
    "prime_factorize",
    "subfactorial",
]


def _require_int(value: object, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} requires an integer")


def _proper_divisor_sum(n: int) -> int:
    if n < 2:
        return 0

    total = 1
    root = math.isqrt(n)
    for divisor in range(2, root + 1):
        if n % divisor == 0:
            total += divisor
            other = n // divisor
            if other != divisor:
                total += other
    return total


def lovelace(
    a: float, b: float, c: float, d: float, e: float, f: float
) -> tuple[float, float]:
    """Lovelace's algorithm for solving systems of linear equations."""
    D = a * e - b * d
    if D == 0:
        raise ValueError("The system has no unique solution.")
    x = (c * e - b * f) / D
    y = (a * f - c * d) / D
    return x, y


def fibonacci_integer(n: int, /) -> int:
    """Return the Fibonacci number at index `n`, where F(0) = 0 and F(1) = 1."""
    _require_int(n, "fibonacci_integer")
    if n < 0:
        raise ValueError("fibonacci_integer requires n >= 0")
    if n < 2:
        return n

    fib0, fib1 = 0, 1
    for _ in range(2, n + 1):
        fib0, fib1 = fib1, fib0 + fib1
    return fib1


def fibonacci_list(n: int, /) -> list[int]:
    """Return the Fibonacci sequence with `n` elements."""
    _require_int(n, "fibonacci_list")
    if n < 0:
        raise ValueError("fibonacci_list requires n >= 0")
    if n == 0:
        return []
    if n == 1:
        return [0]

    sequence = [0, 1]
    for _ in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


def factorial(n: int, /) -> int:
    """Returns the factorial of a non-negative integer `n`."""
    _require_int(n, "factorial")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)


def subfactorial(n: int, /) -> int:
    """Returns the subfactorial of a non-negative integer `n`."""
    _require_int(n, "subfactorial")
    if n < 0:
        raise ValueError("Subfactorial is not defined for negative numbers")
    if n == 0:
        return 1

    previous_two, previous_one = 1, 0
    for k in range(2, n + 1):
        previous_two, previous_one = (
            previous_one,
            (k - 1) * (previous_one + previous_two),
        )
    return previous_one


def gcd(*ints: int) -> int:
    """Returns the greatest common divisor of the given integers."""
    return math.gcd(*ints)


def lcm(*ints: int) -> int:
    """Returns the least common multiple of the given integers."""
    return math.lcm(*ints)


def prime_factorize(n: int, /) -> list[int]:
    """Returns the prime factorization of a number as a list of its prime factors."""
    _require_int(n, "prime_factorize")
    if n < 1:
        raise ValueError("prime_factorize requires n >= 1")

    factors: list[int] = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    divisor = 3
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 2

    if n > 1:
        factors.append(n)

    return factors


def is_prime(n: int, /) -> bool:
    """Returns True if the number is prime, else returns False."""
    _require_int(n, "is_prime")
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def is_perfect_square(n: int, /) -> bool:
    """Returns True if the number is a perfect square, else returns False."""
    _require_int(n, "is_perfect_square")
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def is_perfect_cube(n: int, /) -> bool:
    """Returns True if the number is a perfect cube, else returns False."""
    _require_int(n, "is_perfect_cube")
    magnitude = abs(n)
    c = round(math.cbrt(magnitude))
    return any((c + d) ** 3 == magnitude for d in (-1, 0, 1))


def is_perfect_power(n: int, /) -> bool:
    """Returns True if the number is a perfect power - a number that can be expressed as an integer raised to an integer power - else returns False."""
    _require_int(n, "is_perfect_power")
    if n < 1:
        return False
    for exponent in range(2, int(math.log2(n)) + 1):
        base: int = round(pow(n, 1 / exponent))
        if base**exponent == n:
            return True
    return False


def is_perfect_number(n: int, /) -> bool:
    """Returns True if the number is a perfect number - a number equal to the sum of its proper divisors - else returns False."""
    _require_int(n, "is_perfect_number")
    if n < 1:
        return False
    return _proper_divisor_sum(n) == n


def is_abundant_number(n: int, /) -> bool:
    """Returns True if the number is an abundant number - a number for which the sum of its proper divisors is greater than the number itself - else returns False."""
    _require_int(n, "is_abundant_number")
    if n < 1:
        return False
    return _proper_divisor_sum(n) > n


def is_deficient_number(n: int, /) -> bool:
    """Returns True if the number is a deficient number - a number for which the sum of its proper divisors is less than the number itself - else returns False."""
    _require_int(n, "is_deficient_number")
    if n < 1:
        return False
    return _proper_divisor_sum(n) < n


def is_amicable_pair(a: int, b: int, /) -> bool:
    """Returns True if the numbers are an amicable pair - two numbers for which the sum of the proper divisors of each is equal to the other number - else returns False."""
    _require_int(a, "is_amicable_pair")
    _require_int(b, "is_amicable_pair")
    if a < 1 or b < 1:
        return False
    return _proper_divisor_sum(a) == b and _proper_divisor_sum(b) == a


def is_sociable_chain(chain: list[int]) -> bool:
    """Returns True if the numbers form a sociable chain - a sequence of numbers for which the sum of the proper divisors of each number is equal to the next number in the sequence, and the last number in the sequence is equal to the first number - else returns False."""
    if not isinstance(chain, list):
        raise TypeError("chain must be a list of integers")
    if not chain:
        return False

    for n in chain:
        _require_int(n, "is_sociable_chain")

    if any(n < 1 for n in chain):
        return False

    length = len(chain)
    return all(
        _proper_divisor_sum(n) == chain[(idx + 1) % length]
        for idx, n in enumerate(chain)
    )
