"""Lexicographically Smallest Generated String: a 'T'/'F' string and a lowercase pattern."""


def check(str1: str, str2: str) -> None:
    assert 1 <= len(str1) <= 10**4, "1 <= n == str1.length <= 10^4"
    assert 1 <= len(str2) <= 500, "1 <= m == str2.length <= 500"
    assert all(c in "TF" for c in str1), "str1 consists only of 'T' or 'F'"
    assert all("a" <= c <= "z" for c in str2), "str2 consists only of lowercase English characters"
