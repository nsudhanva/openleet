"""Largest Values From Labels: values with labels, a pick count and a per-label limit."""


def check(values: list[int], labels: list[int], numWanted: int, useLimit: int) -> None:
    n = len(values)
    assert 1 <= n <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert len(labels) == n, "n == values.length == labels.length"
    assert all(0 <= v <= 2 * 10**4 for v in values), "0 <= values[i] <= 2 * 10^4"
    assert all(0 <= v <= 2 * 10**4 for v in labels), "0 <= labels[i] <= 2 * 10^4"
    assert 1 <= numWanted <= n, "1 <= numWanted <= n"
    assert 1 <= useLimit <= n, "1 <= useLimit <= n"
