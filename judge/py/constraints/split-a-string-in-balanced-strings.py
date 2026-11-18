"""Split a String in Balanced Strings: a balanced string of 'L' and 'R'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 2 <= len(s) <= 1000, "2 <= s.length <= 1000"
    assert all(c in "LR" for c in s), "s[i] is either 'L' or 'R'"
    assert s.count("L") == s.count("R"), "s is a balanced string"
