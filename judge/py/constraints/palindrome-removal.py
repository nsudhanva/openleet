"""Palindrome Removal: an array of small positive integers."""


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 100, "1 <= arr.length <= 100"
    assert all(1 <= v <= 20 for v in arr), "1 <= arr[i] <= 20"
