"""Minimum Number of Coins to be Added: coin values and a target."""


def check(coins: list[int], target: int) -> None:
    assert 1 <= target <= 10**5, "1 <= target <= 10^5"
    assert 1 <= len(coins) <= 10**5, "1 <= coins.length <= 10^5"
    assert all(1 <= c <= target for c in coins), "1 <= coins[i] <= target"
