"""Partition Array for Maximum Sum: an integer array and a maximum subarray length k."""


def check(arr: list[int], k: int) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 500, "1 <= arr.length <= 500"
    assert all(0 <= v <= 10**9 for v in arr), "0 <= arr[i] <= 10^9"
    assert 1 <= k <= len(arr), "1 <= k <= arr.length"
