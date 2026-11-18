"""Count Beautiful Substrings: a lowercase string and a positive integer k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 5 * 10**4, "1 <= s.length <= 5 * 10**4"
    assert all("a" <= c <= "z" and len(c) == 1 for c in s), "s is lowercase English letters"
    assert 1 <= k <= 1000, "1 <= k <= 1000"
