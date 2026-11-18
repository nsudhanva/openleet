"""Shortest Common Supersequence: two lowercase strings."""


def check(str1: str, str2: str) -> None:
    assert 1 <= len(str1) <= 1000, "1 <= str1.length <= 1000"
    assert 1 <= len(str2) <= 1000, "1 <= str2.length <= 1000"
    assert all("a" <= ch <= "z" for ch in str1), "str1 consists of lowercase English letters"
    assert all("a" <= ch <= "z" for ch in str2), "str2 consists of lowercase English letters"
