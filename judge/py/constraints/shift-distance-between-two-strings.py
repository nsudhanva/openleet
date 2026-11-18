"""Shift Distance Between Two Strings: two equal-length lowercase strings and two 26-cost lists."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(s: str, t: str, nextCost: list[int], previousCost: list[int]) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert len(s) == len(t), "s.length == t.length"
    assert set(s) <= LOWER, "s consists only of lowercase English letters"
    assert set(t) <= LOWER, "t consists only of lowercase English letters"
    assert len(nextCost) == len(previousCost) == 26, "nextCost.length == previousCost.length == 26"
    assert all(0 <= c <= 10**9 for c in nextCost), "0 <= nextCost[i] <= 10^9"
    assert all(0 <= c <= 10**9 for c in previousCost), "0 <= previousCost[i] <= 10^9"
