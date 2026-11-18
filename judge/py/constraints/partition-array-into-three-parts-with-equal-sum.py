"""Partition Array Into Three Parts With Equal Sum: an integer array."""


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "arr is an array"
    assert 3 <= len(arr) <= 5 * 10**4, "3 <= arr.length <= 5 * 10^4"
    assert all(isinstance(v, int) and -(10**4) <= v <= 10**4 for v in arr), (
        "-10^4 <= arr[i] <= 10^4"
    )
