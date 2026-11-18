"""Unique Number of Occurrences: a list of integers."""


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 1000, "1 <= arr.length <= 1000"
    assert all(isinstance(v, int) and -1000 <= v <= 1000 for v in arr), "-1000 <= arr[i] <= 1000"
