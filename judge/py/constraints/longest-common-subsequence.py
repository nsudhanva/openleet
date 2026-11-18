"""Longest Common Subsequence: two lowercase strings."""


def check(text1: str, text2: str) -> None:
    assert isinstance(text1, str) and isinstance(text2, str), "text1 and text2 are strings"
    assert 1 <= len(text1) <= 1000, "1 <= text1.length <= 1000"
    assert 1 <= len(text2) <= 1000, "1 <= text2.length <= 1000"
    assert all("a" <= c <= "z" for c in text1 + text2), (
        "text1 and text2 consist of only lowercase English characters"
    )
