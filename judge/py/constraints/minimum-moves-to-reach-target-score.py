"""Minimum Moves to Reach Target Score: a target and a maximum number of doublings."""


def check(target: int, maxDoubles: int) -> None:
    assert 1 <= target <= 10**9, "1 <= target <= 10^9"
    assert 0 <= maxDoubles <= 100, "0 <= maxDoubles <= 100"
