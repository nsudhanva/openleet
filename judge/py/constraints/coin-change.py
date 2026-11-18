"""Coin Change: coin denominations and an amount."""


def check(coins: list[int], amount: int) -> None:
    assert 1 <= len(coins) <= 12, "1 <= coins.length <= 12"
    assert all(1 <= c <= 2**31 - 1 for c in coins), "1 <= coins[i] <= 2^31 - 1"
    assert 0 <= amount <= 10**4, "0 <= amount <= 10^4"
