"""Find Latest Group of Size M: a permutation of 1..n giving the order bits are set, and m."""


def check(arr: list[int], m: int) -> None:
    n = len(arr)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= m <= n, "1 <= m <= n"
    assert all(1 <= v <= n for v in arr), "1 <= arr[i] <= n"
    assert len(set(arr)) == n, "all integers in arr are distinct"
