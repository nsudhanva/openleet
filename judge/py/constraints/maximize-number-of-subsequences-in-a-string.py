"""Maximize Number of Subsequences in a String: a text and a 2-letter pattern."""


def check(text: str, pattern: str) -> None:
    assert 1 <= len(text) <= 10**5, "1 <= text.length <= 10^5"
    assert len(pattern) == 2, "pattern.length == 2"
    letters = set("abcdefghijklmnopqrstuvwxyz")
    assert set(text) <= letters, "text consists only of lowercase English letters"
    assert set(pattern) <= letters, "pattern consists only of lowercase English letters"
