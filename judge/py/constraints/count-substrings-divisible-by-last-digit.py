"""Count Substrings Divisible By Last Digit: a string of digits."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert s.isascii() and s.isdigit(), "s consists of digits only"
