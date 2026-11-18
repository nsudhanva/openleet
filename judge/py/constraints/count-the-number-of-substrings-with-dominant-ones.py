"""Count the Number of Substrings With Dominant Ones: a binary string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 4 * 10**4, "1 <= s.length <= 4 * 10^4"
    assert set(s) <= {"0", "1"}, "s consists only of characters '0' and '1'"
