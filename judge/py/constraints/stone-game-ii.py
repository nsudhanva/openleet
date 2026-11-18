"""Stone Game II: a row of piles."""


def check(piles: list[int]) -> None:
    assert 1 <= len(piles) <= 100, "1 <= piles.length <= 100"
    assert all(1 <= v <= 10**4 for v in piles), "1 <= piles[i] <= 10^4"
