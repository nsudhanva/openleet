"""Avoid Flood in The City: daily rains (0 means a dry day)."""


def check(rains: list[int]) -> None:
    assert 1 <= len(rains) <= 10**5, "1 <= rains.length <= 10^5"
    assert all(0 <= v <= 10**9 for v in rains), "0 <= rains[i] <= 10^9"
