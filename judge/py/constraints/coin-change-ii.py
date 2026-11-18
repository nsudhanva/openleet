"""Coin Change II: an amount and distinct coin denominations."""


def check(amount: int, coins: list[int]) -> None:
    assert 1 <= len(coins) <= 300, "1 <= coins.length <= 300"
    assert all(1 <= c <= 5000 for c in coins), "1 <= coins[i] <= 5000"
    assert len(set(coins)) == len(coins), "all the values of coins are unique"
    assert 0 <= amount <= 5000, "0 <= amount <= 5000"
    ways = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    assert ways[amount] < 2**31, "the answer fits into a signed 32-bit integer"
