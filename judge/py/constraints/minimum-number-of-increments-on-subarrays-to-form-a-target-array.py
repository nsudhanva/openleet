"""Minimum Number of Increments on Subarrays to Form a Target Array: a target array."""

from itertools import pairwise


def check(target: list[int]) -> None:
    assert isinstance(target, list), "target is an array"
    assert 1 <= len(target) <= 10**5, "1 <= target.length <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for v in target), "1 <= target[i] <= 10^5"
    ops = target[0] + sum(max(0, b - a) for a, b in pairwise(target))
    assert ops < 2**31, "the answer fits inside a 32 bit integer"
