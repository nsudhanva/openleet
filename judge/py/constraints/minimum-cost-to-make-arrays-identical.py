"""Minimum Cost to Make Arrays Identical: two equal-length integer arrays and a split cost k."""


def check(arr: list[int], brr: list[int], k: int) -> None:
    assert len(arr) == len(brr), "arr.length == brr.length"
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert 0 <= k <= 2 * 10**10, "0 <= k <= 2 * 10^10"
    assert all(-(10**5) <= x <= 10**5 for x in arr), "-10^5 <= arr[i] <= 10^5"
    assert all(-(10**5) <= x <= 10**5 for x in brr), "-10^5 <= brr[i] <= 10^5"
