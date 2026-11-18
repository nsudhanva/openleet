"""Number of Sub-arrays With Odd Sum: an array of small positive integers."""


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(1 <= v <= 100 for v in arr), "1 <= arr[i] <= 100"
