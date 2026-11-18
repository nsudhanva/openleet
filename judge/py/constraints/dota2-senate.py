"""Dota2 Senate: a string of 'R' and 'D' senators."""


def check(senate: str) -> None:
    assert isinstance(senate, str), "string"
    assert 1 <= len(senate) <= 10**4, "1 <= n <= 10^4"
    assert all(c in "RD" for c in senate), "senate[i] is either 'R' or 'D'"
