"""Valid Mountain Array: a list of non-negative integers."""


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 10**4, "1 <= arr.length <= 10^4"
    assert all(isinstance(v, int) and 0 <= v <= 10**4 for v in arr), "0 <= arr[i] <= 10^4"
