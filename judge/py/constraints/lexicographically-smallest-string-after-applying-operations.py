"""Lexicographically Smallest String After Applying Operations: an even-length digit string
and two operation sizes."""


def check(s: str, a: int, b: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 2 <= len(s) <= 100, "2 <= s.length <= 100"
    assert len(s) % 2 == 0, "s.length is even"
    assert all("0" <= c <= "9" for c in s), "s consists of digits from 0 to 9 only"
    assert 1 <= a <= 9, "1 <= a <= 9"
    assert 1 <= b <= len(s) - 1, "1 <= b <= s.length - 1"
