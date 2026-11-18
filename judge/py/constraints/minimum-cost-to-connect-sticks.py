"""Minimum Cost to Connect Sticks: a list of stick lengths."""


def check(sticks: list[int]) -> None:
    assert 1 <= len(sticks) <= 10**4, "1 <= sticks.length <= 10^4"
    assert all(1 <= s <= 10**4 for s in sticks), "1 <= sticks[i] <= 10^4"
