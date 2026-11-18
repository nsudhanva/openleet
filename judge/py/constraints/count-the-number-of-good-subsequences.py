"""Count the Number of Good Subsequences: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert s.isascii() and s.islower() and s.isalpha(), "s consists of lowercase English letters"
