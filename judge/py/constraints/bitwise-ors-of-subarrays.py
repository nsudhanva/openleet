"""Bitwise ORs of Subarrays: an array of non-negative integers."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 5 * 10**4, "1 <= arr.length <= 5 * 10^4"
    assert all(0 <= v <= 10**9 for v in arr), "0 <= arr[i] <= 10^9"
