"""Rotate String: two lowercase strings."""


def check(s: str, goal: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert 1 <= len(goal) <= 100, "1 <= goal.length <= 100"
    assert all("a" <= c <= "z" for c in s + goal), "s and goal consist of lowercase English letters"
