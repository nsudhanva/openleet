"""Kth Missing Positive Number: a strictly increasing array of positive integers and k."""

from itertools import pairwise


def check(arr: list[int], k: int) -> None:
    assert 1 <= len(arr) <= 1000, "1 <= arr.length <= 1000"
    assert all(1 <= v <= 1000 for v in arr), "1 <= arr[i] <= 1000"
    assert 1 <= k <= 1000, "1 <= k <= 1000"
    assert all(a < b for a, b in pairwise(arr)), "arr is strictly increasing"
