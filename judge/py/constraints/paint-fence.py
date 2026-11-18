"""Paint Fence: n posts and k colors, with no three consecutive posts the same color."""


def check(n: int, k: int) -> None:
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
    same, diff = 0, k
    for _ in range(n - 1):
        same, diff = diff, (same + diff) * (k - 1)
    assert 0 <= same + diff <= 2**31 - 1, "the answer is in the range [0, 2^31 - 1]"
