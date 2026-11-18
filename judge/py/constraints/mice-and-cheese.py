"""Mice and Cheese: two reward arrays of equal length and a count k."""


def check(reward1: list[int], reward2: list[int], k: int) -> None:
    n = len(reward1)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(reward2) == n, "reward1.length == reward2.length"
    assert all(1 <= v <= 1000 for v in reward1), "1 <= reward1[i] <= 1000"
    assert all(1 <= v <= 1000 for v in reward2), "1 <= reward2[i] <= 1000"
    assert 0 <= k <= n, "0 <= k <= n"
