"""Minimum Moves to Balance Circular Array: a circular array with at most one negative value."""


def check(balance: list[int]) -> None:
    assert 1 <= len(balance) <= 10**5, "1 <= n == balance.length <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in balance), "-10^9 <= balance[i] <= 10^9"
    assert sum(v < 0 for v in balance) <= 1, "There is at most one negative value in balance"
