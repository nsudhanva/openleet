"""Maximum Product of the Length of Two Palindromic Subsequences: a lowercase string."""


def check(s: str) -> None:
    assert 2 <= len(s) <= 12, "2 <= s.length <= 12"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters only"
