"""Count Substrings That Differ by One Character: two lowercase strings."""


def check(s: str, t: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert 1 <= len(t) <= 100, "1 <= t.length <= 100"
    assert s.isascii() and s.islower() and s.isalpha(), "s is lowercase English letters"
    assert t.isascii() and t.islower() and t.isalpha(), "t is lowercase English letters"
