"""Distinct Echo Substrings: a lowercase string."""


def check(text: str) -> None:
    assert 1 <= len(text) <= 2000, "1 <= text.length <= 2000"
    assert all("a" <= c <= "z" for c in text), "text has only lowercase English letters"
