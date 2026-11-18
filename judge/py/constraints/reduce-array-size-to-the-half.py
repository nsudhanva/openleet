"""Reduce Array Size to The Half: an even-length array of positive integers."""


def check(arr: list[int]) -> None:
    assert 2 <= len(arr) <= 10**5, "2 <= arr.length <= 10^5"
    assert len(arr) % 2 == 0, "arr.length is even"
    assert all(1 <= v <= 10**5 for v in arr), "1 <= arr[i] <= 10^5"
