"""Stone Game: an even number of piles with an odd total."""


def check(piles: list[int]) -> None:
    assert 2 <= len(piles) <= 500, "2 <= piles.length <= 500"
    assert len(piles) % 2 == 0, "piles.length is even"
    assert all(1 <= v <= 500 for v in piles), "1 <= piles[i] <= 500"
    assert sum(piles) % 2 == 1, "sum(piles[i]) is odd"
