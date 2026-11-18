"""Valid Palindrome: a printable ASCII string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 2 * 10**5, "1 <= s.length <= 2 * 10^5"
    assert all(32 <= ord(c) <= 126 for c in s), "s consists only of printable ASCII characters"
