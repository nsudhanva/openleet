"""Element Appearing More Than 25% In Sorted Array: a sorted array with one
majority-quarter value."""

from collections import Counter


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "list"
    assert 1 <= len(arr) <= 10**4, "1 <= arr.length <= 10^4"
    assert all(isinstance(v, int) and 0 <= v <= 10**5 for v in arr), "0 <= arr[i] <= 10^5"
    assert all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)), "sorted in non-decreasing order"
    big = [v for v, c in Counter(arr).items() if 4 * c > len(arr)]
    assert len(big) == 1, "exactly one integer occurs more than 25% of the time"
