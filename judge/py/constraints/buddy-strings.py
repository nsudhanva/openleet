"""Buddy Strings: two lowercase strings."""


def check(s: str, goal: str) -> None:
    assert isinstance(s, str) and isinstance(goal, str), "s and goal are strings"
    assert 1 <= len(s) <= 2 * 10**4, "1 <= s.length <= 2 * 10^4"
    assert 1 <= len(goal) <= 2 * 10**4, "1 <= goal.length <= 2 * 10^4"
    assert all("a" <= c <= "z" for c in s + goal), "s and goal consist of lowercase letters"
