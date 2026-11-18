"""Check if All A's Appears Before All B's: a string of 'a' and 'b'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c in "ab" for c in s), "s[i] is either 'a' or 'b'"
