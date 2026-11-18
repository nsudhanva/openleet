"""Jump Game III: an array of jump lengths and a start index."""


def check(arr: list[int], start: int) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 5 * 10**4, "1 <= arr.length <= 5 * 10^4"
    assert all(0 <= v < len(arr) for v in arr), "0 <= arr[i] < arr.length"
    assert 0 <= start < len(arr), "0 <= start < arr.length"
