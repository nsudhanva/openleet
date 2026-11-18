"""Shortest Subarray to be Removed to Make Array Sorted: an array of non-negative integers."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(0 <= x <= 10**9 for x in arr), "0 <= arr[i] <= 10^9"
