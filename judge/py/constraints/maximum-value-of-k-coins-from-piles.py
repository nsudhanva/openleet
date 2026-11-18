"""Maximum Value of K Coins From Piles: piles of coin values and a count k."""


def check(piles: list[list[int]], k: int) -> None:
    assert 1 <= len(piles) <= 1000, "1 <= n <= 1000"
    assert all(1 <= v <= 10**5 for p in piles for v in p), "1 <= piles[i][j] <= 10^5"
    assert 1 <= k <= sum(len(p) for p in piles) <= 2000, "1 <= k <= sum(piles[i].length) <= 2000"
