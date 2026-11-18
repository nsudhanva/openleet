"""Remove Stones to Minimize the Total: pile sizes and an operation count k."""


def check(piles: list[int], k: int) -> None:
    assert isinstance(piles, list), "piles is a list"
    assert isinstance(k, int), "k is an integer"
    assert 1 <= len(piles) <= 10**5, "1 <= piles.length <= 10^5"
    assert all(1 <= p <= 10**4 for p in piles), "1 <= piles[i] <= 10^4"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
