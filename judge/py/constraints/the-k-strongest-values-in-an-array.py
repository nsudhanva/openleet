"""The k Strongest Values in an Array: an integer array and k."""


def check(arr: list[int], k: int) -> None:
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(-(10**5) <= x <= 10**5 for x in arr), "-10^5 <= arr[i] <= 10^5"
    assert 1 <= k <= len(arr), "1 <= k <= arr.length"
