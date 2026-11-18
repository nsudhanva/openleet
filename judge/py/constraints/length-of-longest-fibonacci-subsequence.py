"""Length of Longest Fibonacci Subsequence: a strictly increasing integer array."""

import itertools


def check(arr: list[int]) -> None:
    assert 3 <= len(arr) <= 1000, "3 <= arr.length <= 1000"
    assert all(1 <= v <= 10**9 for v in arr), "1 <= arr[i] <= 10^9"
    assert all(a < b for a, b in itertools.pairwise(arr)), "arr[i] < arr[i + 1]"
