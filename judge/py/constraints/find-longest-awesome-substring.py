"""Find Longest Awesome Substring: a string of digits."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "0123456789" for c in s), "s consists only of digits"
