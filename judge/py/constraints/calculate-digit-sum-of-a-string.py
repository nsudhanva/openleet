"""Calculate Digit Sum of a String: a digit string and a group size k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert 2 <= k <= 100, "2 <= k <= 100"
    assert s.isascii() and s.isdigit(), "s consists of digits only"
