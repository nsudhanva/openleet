"""Divide Chocolate: chunk sweetness values and the number of friends k."""


def check(sweetness: list[int], k: int) -> None:
    assert 0 <= k < len(sweetness) <= 10**4, "0 <= k < sweetness.length <= 10^4"
    assert all(1 <= v <= 10**5 for v in sweetness), "1 <= sweetness[i] <= 10^5"
