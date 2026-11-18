"""Split a String Into the Max Number of Unique Substrings: a short lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 16, "1 <= s.length <= 16"
    assert all("a" <= c <= "z" for c in s), "s contains only lower case English letters"
