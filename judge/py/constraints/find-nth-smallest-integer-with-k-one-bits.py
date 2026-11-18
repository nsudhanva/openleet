"""Find Nth Smallest Integer With K One Bits: positive n and k."""

from math import comb


def check(n: int, k: int) -> None:
    assert 1 <= n <= 2**50, "1 <= n <= 2^50"
    assert 1 <= k <= 50, "1 <= k <= 50"
    # Integers below 2^50 with exactly k one bits number C(50, k).
    assert n <= comb(50, k), "the answer is strictly less than 2^50"
