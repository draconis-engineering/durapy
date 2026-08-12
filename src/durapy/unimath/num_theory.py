"""`UniMath` Number Theory source"""

import math


def lovelace(
    a: float, b: float, c: float, d: float, e: float, f: float
) -> tuple[float, float]:
    """Lovelace's algorithm for solving systems of linear equations."""
    D = a * e - b * d
    if D == 0:
        raise ValueError("The system has no unique solution.")
    x = c * e - b * f / D
    y = a * f - c * d / D
    return x, y


def fibonacci_integer(fib_idx: int) -> int:
    """Fibonacci integer generator that returns the Fibonacci integer at the given index."""

    if fib_idx < 2 or not isinstance(fib_idx, int):
        raise ValueError(
            "fibonacci_integer does not take integers less than 2 or floats/strings!"
        )

    if fib_idx == 2:
        return 1

    fib0, fib1, fib2 = 0, 1, 1

    for _ in range(fib_idx - 2):
        fib2 = fib0 + fib1
        fib0, fib1 = fib1, fib2

    return fib2


def fibonacci_list(n: int) -> list[int]:
    """Fibonacci sequence generator that returns a list of the sequence up to the given length."""

    if n < 2 or not isinstance(n, int):
        raise ValueError(
            "fibonacci_list does not take integers less than 2 or floats/strings!"
        )

    if n == 2:
        return [0, 1]

    fib0, fib1, fiblist = 0, 1, [0, 1]

    for _ in range(n - 2):
        fib2 = fib0 + fib1
        fib0, fib1 = fib1, fib2
        fiblist.append(fib2)

    return fiblist


def factorial(n: int) -> int:
    """Returns the factorial of a non-negative integer `n`."""
    if n < 0 or not isinstance(n, int):
        raise ValueError(
            "Factorial is not defined for negative numbers or floats/strings!"
        )

    elif n == 0 or n == 1:
        return 1

    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


def subfactorial(n: int) -> int:
    """Returns the subfactorial of a non-negative integer `n`."""
    if n < 0 or not isinstance(n, int):
        raise ValueError(
            "Subfactorial and Factorial are not defined for negative numbers or floats/strings!"
        )
    return int(factorial(n) * sum((-1) ** k / factorial(k) for k in range(n)))


def gcd(*ints: int) -> int:
    """Returns the greatest common divisor of the given integers."""
    return math.gcd(*ints)


def lcm(*ints: int) -> int:
    """Returns the least common multiple of the given integers."""
    return abs(math.prod(ints)) // gcd(*ints)


def prime_factorize(n: int) -> list[int]:
    """Returns the prime factorization of a number as a list of its prime factors."""
    factors: list[int] = []
    div = 2

    while n >= 2:
        if n % div == 0:
            factors.append(div)
            n //= div
        else:
            div += 1

    return factors


def is_prime(n: int) -> bool:
    """Returns True if the number is prime, else returns False."""
    if n <= 1:
        return False
    if n == 2:
        return True
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect_square(n: int) -> bool:
    """Returns True if the number is a perfect square, else returns False."""
    if n < 0:
        return False
    return int(math.sqrt(n)) ** 2 == n


def is_perfect_cube(n: int) -> bool:
    """Returns True if the number is a perfect cube, else returns False."""
    if n < 0:
        return False
    return math.pow(math.sqrt(n), 3) == n


def is_perfect_power(n: int) -> bool:
    """Returns True if the number is a perfect power - a number that can be expressed as an integer raised to an integer power - else returns False."""
    if n < 1:
        return False
    for b in range(2, int(math.log2(n)) + 1):
        a: int = round(pow(n, 1 / b))
        if a**b == n:
            return True
    return False


def is_perfect_number(n: int) -> bool:
    """Returns True if the number is a perfect number - a number equal to the sum of its proper divisors - else returns False."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n


def is_abundant_number(n: int) -> bool:
    """Returns True if the number is an abundant number - a number for which the sum of its proper divisors is greater than the number itself - else returns False."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) > n


def is_deficient_number(n: int) -> bool:
    """Returns True if the number is a deficient number - a number for which the sum of its proper divisors is less than the number itself - else returns False."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) < n


def is_amicable_pair(a: int, b: int) -> bool:
    """Returns True if the numbers are an amicable pair - two numbers for which the sum of the proper divisors of each is equal to the other number - else returns False."""
    if a < 1 or b < 1:
        return False
    return (
        sum(i for i in range(1, a) if a % i == 0) == b
        and sum(i for i in range(1, b) if b % i == 0) == a
    )


def is_sociable_chain(chain: list[int]) -> bool:
    """Returns True if the numbers form a sociable chain - a sequence of numbers for which the sum of the proper divisors of each number is equal to the next number in the sequence, and the last number in the sequence is equal to the first number - else returns False."""
    if any(n < 1 for n in chain):
        return False
    return all(
        sum(i for i in range(1, n) if n % i == 0) == chain[(idx + 1) % len(chain)]
        for idx, n in enumerate(chain)
    )
