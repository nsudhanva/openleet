"""Minimum Absolute Difference: a list of distinct integers."""


def check(arr: list[int]) -> None:
    assert 2 <= len(arr) <= 10**5, "2 <= arr.length <= 10^5"
    assert all(-(10**6) <= v <= 10**6 for v in arr), "-10^6 <= arr[i] <= 10^6"
    assert len(set(arr)) == len(arr), "arr consists of distinct integers"
