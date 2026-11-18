"""Least Number of Unique Integers after K Removals: an integer array and a removal count."""


def check(arr: list[int], k: int) -> None:
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in arr), "1 <= arr[i] <= 10^9"
    assert 0 <= k <= len(arr), "0 <= k <= arr.length"
