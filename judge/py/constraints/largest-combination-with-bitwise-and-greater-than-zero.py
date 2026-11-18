"""Largest Combination With Bitwise AND Greater Than Zero: an array of positive integers."""


def check(candidates: list[int]) -> None:
    assert 1 <= len(candidates) <= 10**5, "1 <= candidates.length <= 10^5"
    assert all(1 <= v <= 10**7 for v in candidates), "1 <= candidates[i] <= 10^7"
