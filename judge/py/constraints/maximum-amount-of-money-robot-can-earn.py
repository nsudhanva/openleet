"""Maximum Amount of Money Robot Can Earn: an m x n grid of coin values."""


def check(coins: list[list[int]]) -> None:
    m = len(coins)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(coins[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(row) == n for row in coins), "n == coins[i].length"
    assert all(-1000 <= v <= 1000 for row in coins for v in row), "-1000 <= coins[i][j] <= 1000"
