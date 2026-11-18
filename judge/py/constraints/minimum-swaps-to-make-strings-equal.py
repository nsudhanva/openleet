"""Minimum Swaps to Make Strings Equal: two equal-length strings over 'x' and 'y'."""


def check(s1: str, s2: str) -> None:
    assert 1 <= len(s1) <= 1000, "1 <= s1.length <= 1000"
    assert 1 <= len(s2) <= 1000, "1 <= s2.length <= 1000"
    assert len(s1) == len(s2), "s1.length == s2.length"
    assert set(s1) <= {"x", "y"}, "s1 only contains 'x' or 'y'"
    assert set(s2) <= {"x", "y"}, "s2 only contains 'x' or 'y'"
