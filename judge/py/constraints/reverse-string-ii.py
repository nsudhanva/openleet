"""Reverse String II: a lowercase string and a block size k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
    assert 1 <= k <= 10**4, "1 <= k <= 10^4"
