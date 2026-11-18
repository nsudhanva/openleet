"""Longest Mountain in Array: an int array."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 10**4, "1 <= arr.length <= 10^4"
    assert all(0 <= v <= 10**4 for v in arr), "0 <= arr[i] <= 10^4"
