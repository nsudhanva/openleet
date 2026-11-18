"""Shortest and Lexicographically Smallest Beautiful String: a binary string and a count k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert set(s) <= {"0", "1"}, "s is a binary string"
    assert 1 <= k <= len(s), "1 <= k <= s.length"
