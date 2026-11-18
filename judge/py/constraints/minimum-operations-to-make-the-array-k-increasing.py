"""Minimum Operations to Make the Array K-Increasing: an array arr and a step k."""


def check(arr: list[int], k: int) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(1 <= x <= len(arr) for x in arr), "1 <= arr[i] <= arr.length"
    assert 1 <= k <= len(arr), "1 <= k <= arr.length"
