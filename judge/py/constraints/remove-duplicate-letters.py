"""Remove Duplicate Letters: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
