"""Sum of Subarray Minimums: an integer array."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 30000, "1 <= arr.length <= 30000"
    assert all(1 <= v <= 30000 for v in arr), "1 <= arr[i] <= 3 * 10^4"
