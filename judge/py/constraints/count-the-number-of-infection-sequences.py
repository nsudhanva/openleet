"""Count the Number of Infection Sequences: n people and the sorted positions of the sick."""

from itertools import pairwise


def check(n: int, sick: list[int]) -> None:
    assert isinstance(sick, list), "sick is a list"
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= len(sick) <= n - 1, "1 <= sick.length <= n - 1"
    assert all(0 <= v <= n - 1 for v in sick), "0 <= sick[i] <= n - 1"
    assert all(a < b for a, b in pairwise(sick)), "sick is sorted in increasing order"
