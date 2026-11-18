"""Richest Customer Wealth: an m x n grid of account balances."""


def check(accounts: list[list[int]]) -> None:
    m = len(accounts)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(accounts[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(r) == n for r in accounts), "n == accounts[i].length"
    assert all(1 <= v <= 100 for r in accounts for v in r), "1 <= accounts[i][j] <= 100"
