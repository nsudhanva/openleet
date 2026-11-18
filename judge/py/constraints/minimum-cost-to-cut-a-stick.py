"""Minimum Cost to Cut a Stick: a stick length n and distinct cut positions."""


def check(n: int, cuts: list[int]) -> None:
    assert 2 <= n <= 10**6, "2 <= n <= 10^6"
    assert 1 <= len(cuts) <= min(n - 1, 100), "1 <= cuts.length <= min(n - 1, 100)"
    assert all(1 <= c <= n - 1 for c in cuts), "1 <= cuts[i] <= n - 1"
    assert len(set(cuts)) == len(cuts), "all integers in cuts are distinct"
