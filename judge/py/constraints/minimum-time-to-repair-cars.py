"""Minimum Time to Repair Cars: mechanic ranks and a car count."""


def check(ranks: list[int], cars: int) -> None:
    assert 1 <= len(ranks) <= 10**5, "1 <= ranks.length <= 10^5"
    assert all(1 <= v <= 100 for v in ranks), "1 <= ranks[i] <= 100"
    assert 1 <= cars <= 10**6, "1 <= cars <= 10^6"
