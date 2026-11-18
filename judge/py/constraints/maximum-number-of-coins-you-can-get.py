"""Maximum Number of Coins You Can Get: pile sizes, count a multiple of 3."""


def check(piles: list[int]) -> None:
    assert 3 <= len(piles) <= 10**5, "3 <= piles.length <= 10^5"
    assert len(piles) % 3 == 0, "piles.length % 3 == 0"
    assert all(1 <= v <= 10**4 for v in piles), "1 <= piles[i] <= 10^4"
