"""Sum of All Odd Length Subarrays: an array of positive integers."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 100, "1 <= arr.length <= 100"
    assert all(1 <= x <= 1000 for x in arr), "1 <= arr[i] <= 1000"
