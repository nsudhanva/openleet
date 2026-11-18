"""Number of Steps to Reduce a Number in Binary Representation to One: a binary string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 500, "1 <= s.length <= 500"
    assert set(s) <= {"0", "1"}, "s consists of '0' or '1'"
    assert s[0] == "1", "s[0] == '1'"
