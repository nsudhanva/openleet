"""Longest Chunked Palindrome Decomposition: a lowercase string."""


def check(text: str) -> None:
    assert isinstance(text, str), "text is a string"
    assert 1 <= len(text) <= 1000, "1 <= text.length <= 1000"
    assert all("a" <= c <= "z" for c in text), "text consists only of lowercase English characters"
