"""Count Beautiful Substrings: a lowercase string and a positive integer k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 10**3, "1 <= s.length <= 10**3"
    assert all("a" <= c <= "z" and len(c) == 1 for c in s), "s is lowercase English letters"
    assert 1 <= k <= 1000, "1 <= k <= 1000"
