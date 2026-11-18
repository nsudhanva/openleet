"""Maximum Number of Integers to Choose From a Range I: banned values, a range limit n and a
max sum."""


def check(banned: list[int], n: int, maxSum: int) -> None:
    assert 1 <= len(banned) <= 10**4, "1 <= banned.length <= 10^4"
    assert all(1 <= v <= 10**4 for v in banned), "1 <= banned[i] <= 10^4"
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 1 <= maxSum <= 10**9, "1 <= maxSum <= 10^9"
