"""Count Different Palindromic Subsequences: a string over a, b, c, d."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all(c in ("a", "b", "c", "d") for c in s), "s[i] is 'a', 'b', 'c' or 'd'"
