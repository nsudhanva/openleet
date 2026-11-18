"""Max Chunks To Make Sorted II: an array of non-negative integers."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 2000, "1 <= arr.length <= 2000"
    assert all(0 <= v <= 10**8 for v in arr), "0 <= arr[i] <= 10^8"
