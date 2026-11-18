"""Matchsticks to Square: a list of matchstick lengths."""


def check(matchsticks: list[int]) -> None:
    assert 1 <= len(matchsticks) <= 15, "1 <= matchsticks.length <= 15"
    assert all(1 <= v <= 10**8 for v in matchsticks), "1 <= matchsticks[i] <= 10^8"
