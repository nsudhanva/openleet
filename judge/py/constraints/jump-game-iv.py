"""Jump Game IV: an integer array."""


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 5 * 10**4, "1 <= arr.length <= 5 * 10^4"
    assert all(-(10**8) <= v <= 10**8 for v in arr), "-10^8 <= arr[i] <= 10^8"
