"""Lexicographically Smallest String After Deleting Duplicate Characters: a lowercase
string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s contains lowercase English letters only"
