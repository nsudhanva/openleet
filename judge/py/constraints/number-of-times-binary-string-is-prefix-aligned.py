"""Number of Times Binary String Is Prefix-Aligned: a permutation of 1..n."""


def check(flips: list[int]) -> None:
    assert isinstance(flips, list), "flips is a list"
    n = len(flips)
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert sorted(flips) == list(range(1, n + 1)), "flips is a permutation of [1, n]"
