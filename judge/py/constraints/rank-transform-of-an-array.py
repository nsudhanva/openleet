"""Rank Transform of an Array: a list of integers."""


def check(arr: list[int]) -> None:
    assert 0 <= len(arr) <= 10**5, "0 <= arr.length <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in arr), "-10^9 <= arr[i] <= 10^9"
