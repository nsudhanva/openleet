"""Check If Array Pairs Are Divisible by k: an even-length integer array and k."""


def check(arr: list[int], k: int) -> None:
    n = len(arr)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert n % 2 == 0, "n is even"
    assert all(-(10**9) <= v <= 10**9 for v in arr), "-10^9 <= arr[i] <= 10^9"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
