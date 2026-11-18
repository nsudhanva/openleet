"""Duplicate Zeros: an array of digits 0..9."""


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "list"
    assert 1 <= len(arr) <= 10**4, "1 <= arr.length <= 10^4"
    assert all(isinstance(v, int) and 0 <= v <= 9 for v in arr), "0 <= arr[i] <= 9"
