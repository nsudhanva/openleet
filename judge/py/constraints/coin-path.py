"""Coin Path: 1-indexed coin costs (-1 blocked) and a maximum jump."""


def check(coins: list[int], maxJump: int) -> None:
    assert 1 <= len(coins) <= 1000, "1 <= coins.length <= 1000"
    assert all(-1 <= c <= 100 for c in coins), "-1 <= coins[i] <= 100"
    assert coins[0] != -1, "coins[1] != -1"
    assert 1 <= maxJump <= 100, "1 <= maxJump <= 100"
