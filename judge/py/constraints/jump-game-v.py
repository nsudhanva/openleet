"""Jump Game V: an array of heights and a maximum jump distance d."""


def check(arr: list[int], d: int) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 1000, "1 <= arr.length <= 1000"
    assert all(1 <= v <= 10**5 for v in arr), "1 <= arr[i] <= 10^5"
    assert 1 <= d <= len(arr), "1 <= d <= arr.length"
