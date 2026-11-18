"""Super Ugly Number: an index n and a sorted list of distinct primes."""

from itertools import pairwise


def _is_prime(p: int) -> bool:
    return p >= 2 and all(p % d for d in range(2, int(p**0.5) + 1))


def check(n: int, primes: list[int]) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(primes) <= 100, "1 <= primes.length <= 100"
    assert all(2 <= p <= 1000 for p in primes), "2 <= primes[i] <= 1000"
    assert all(_is_prime(p) for p in primes), "primes[i] is a prime number"
    assert all(a < b for a, b in pairwise(primes)), "primes are unique and ascending"
