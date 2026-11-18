"""Longest Arithmetic Subsequence of Given Difference: an integer array and a difference."""


def check(arr: list[int], difference: int) -> None:
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(-(10**4) <= v <= 10**4 for v in arr), "-10^4 <= arr[i] <= 10^4"
    assert -(10**4) <= difference <= 10**4, "-10^4 <= difference <= 10^4"
