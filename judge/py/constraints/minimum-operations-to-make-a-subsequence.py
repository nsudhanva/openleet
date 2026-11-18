"""Minimum Operations to Make a Subsequence: a duplicate-free target and an array arr."""


def check(target: list[int], arr: list[int]) -> None:
    assert isinstance(target, list) and isinstance(arr, list), "target and arr are lists"
    assert 1 <= len(target) <= 10**5, "1 <= target.length <= 10^5"
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(1 <= x <= 10**9 for x in target), "1 <= target[i] <= 10^9"
    assert all(1 <= x <= 10**9 for x in arr), "1 <= arr[i] <= 10^9"
    assert len(set(target)) == len(target), "target contains no duplicates"
