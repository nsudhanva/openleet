"""Build an Array With Stack Operations: a strictly increasing target and n."""

from itertools import pairwise


def check(target: list[int], n: int) -> None:
    assert 1 <= len(target) <= 100, "1 <= target.length <= 100"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(1 <= t <= n for t in target), "1 <= target[i] <= n"
    assert all(a < b for a, b in pairwise(target)), "target is strictly increasing"
