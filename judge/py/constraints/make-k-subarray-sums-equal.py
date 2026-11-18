"""Make K-Subarray Sums Equal: a circular array and a window size k."""


def check(arr: list[int], k: int) -> None:
    assert 1 <= k <= len(arr) <= 10**5, "1 <= k <= arr.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in arr), "1 <= arr[i] <= 10^9"
