"""Kth Smallest Amount With Single Denomination Combination: distinct coin values and k."""


def check(coins: list[int], k: int) -> None:
    assert 1 <= len(coins) <= 15, "1 <= coins.length <= 15"
    assert all(1 <= v <= 25 for v in coins), "1 <= coins[i] <= 25"
    assert 1 <= k <= 2 * 10**9, "1 <= k <= 2 * 10^9"
    assert len(set(coins)) == len(coins), "coins contains pairwise distinct integers"
