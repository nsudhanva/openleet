"""Koko Eating Bananas: banana piles and the hours h."""


def check(piles: list[int], h: int) -> None:
    assert 1 <= len(piles) <= 10**4, "1 <= piles.length <= 10^4"
    assert len(piles) <= h <= 10**9, "piles.length <= h <= 10^9"
    assert all(1 <= v <= 10**9 for v in piles), "1 <= piles[i] <= 10^9"
