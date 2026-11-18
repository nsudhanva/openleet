"""Maximize Happiness of Selected Children: a list of happiness values and k."""


def check(happiness: list[int], k: int) -> None:
    n = len(happiness)
    assert 1 <= n <= 2 * 10**5, "1 <= n == happiness.length <= 2 * 10^5"
    assert all(1 <= h <= 10**8 for h in happiness), "1 <= happiness[i] <= 10^8"
    assert 1 <= k <= n, "1 <= k <= n"
