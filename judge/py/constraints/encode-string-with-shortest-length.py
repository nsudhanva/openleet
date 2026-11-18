"""Encode String with Shortest Length: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "string"
    assert 1 <= len(s) <= 150, "1 <= s.length <= 150"
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
