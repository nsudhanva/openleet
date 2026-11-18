"""Minimum Adjacent Swaps to Reach the Kth Smallest Number: a digit string and k."""


def check(num: str, k: int) -> None:
    assert isinstance(num, str), "num is a string"
    assert 2 <= len(num) <= 1000, "2 <= num.length <= 1000"
    assert 1 <= k <= 1000, "1 <= k <= 1000"
    assert all(c in "0123456789" for c in num), "num only consists of digits"
    d = list(num)
    n = len(d)
    for _ in range(k):
        i = n - 2
        while i >= 0 and d[i] >= d[i + 1]:
            i -= 1
        assert i >= 0, "the kth smallest wonderful integer exists"
        j = n - 1
        while d[j] <= d[i]:
            j -= 1
        d[i], d[j] = d[j], d[i]
        d[i + 1 :] = reversed(d[i + 1 :])
