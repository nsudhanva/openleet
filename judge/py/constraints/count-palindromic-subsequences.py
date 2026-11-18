"""Count Palindromic Subsequences: a string of digits."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all("0" <= c <= "9" for c in s), "s consists of digits"
