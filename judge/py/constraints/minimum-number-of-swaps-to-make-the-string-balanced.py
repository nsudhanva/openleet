"""Minimum Number of Swaps to Make the String Balanced: an even-length string of brackets with
equal opening and closing counts."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    n = len(s)
    assert 2 <= n <= 10**6, "2 <= n <= 10^6"
    assert n % 2 == 0, "n is even"
    assert set(s) <= {"[", "]"}, "s[i] is either '[' or ']'"
    assert s.count("[") == n // 2, "the number of '[' equals n / 2"
    assert s.count("]") == n // 2, "the number of ']' equals n / 2"
