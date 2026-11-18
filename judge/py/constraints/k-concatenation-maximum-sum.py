"""K-Concatenation Maximum Sum: an integer array and a repeat count k."""


def check(arr: list[int], k: int) -> None:
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
    assert all(-(10**4) <= v <= 10**4 for v in arr), "-10^4 <= arr[i] <= 10^4"
