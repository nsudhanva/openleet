"""Number of Sub-arrays of Size K and Average >= Threshold: array, k, threshold."""


def check(arr: list[int], k: int, threshold: int) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(1 <= v <= 10**4 for v in arr), "1 <= arr[i] <= 10^4"
    assert 1 <= k <= len(arr), "1 <= k <= arr.length"
    assert 0 <= threshold <= 10**4, "0 <= threshold <= 10^4"
