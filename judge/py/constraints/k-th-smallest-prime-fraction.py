"""K-th Smallest Prime Fraction: a sorted array of 1 and distinct primes, and k."""

from itertools import pairwise


def _is_prime(v: int) -> bool:
    if v < 2:
        return False
    i = 2
    while i * i <= v:
        if v % i == 0:
            return False
        i += 1
    return True


def check(arr: list[int], k: int) -> None:
    n = len(arr)
    assert 2 <= n <= 1000, "2 <= arr.length <= 1000"
    assert all(1 <= v <= 3 * 10**4 for v in arr), "1 <= arr[i] <= 3 * 10^4"
    assert arr[0] == 1, "arr[0] == 1"
    assert all(_is_prime(v) for v in arr[1:]), "arr[i] is a prime number for i > 0"
    assert all(a < b for a, b in pairwise(arr)), "arr is unique and strictly increasing"
    assert 1 <= k <= n * (n - 1) // 2, "1 <= k <= arr.length * (arr.length - 1) / 2"
