"""Candy: children's ratings."""


def check(ratings: list[int]) -> None:
    assert 1 <= len(ratings) <= 5 * 10**4, "1 <= n == ratings.length <= 5 * 10^4"
    assert all(0 <= r <= 5 * 10**4 for r in ratings), "0 <= ratings[i] <= 5 * 10^4"
