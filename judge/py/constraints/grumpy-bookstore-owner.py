"""Grumpy Bookstore Owner: customers per minute, grumpy flags and a window length."""


def check(customers: list[int], grumpy: list[int], minutes: int) -> None:
    n = len(customers)
    assert n == len(grumpy), "n == customers.length == grumpy.length"
    assert 1 <= minutes <= n <= 2 * 10**4, "1 <= minutes <= n <= 2 * 10^4"
    assert all(0 <= c <= 1000 for c in customers), "0 <= customers[i] <= 1000"
    assert all(g in (0, 1) for g in grumpy), "grumpy[i] is either 0 or 1"
