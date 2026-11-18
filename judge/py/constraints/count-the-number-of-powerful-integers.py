"""Count the Number of Powerful Integers: a range [start, finish], a digit limit and suffix s."""


def check(start: int, finish: int, limit: int, s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= start <= finish <= 10**15, "1 <= start <= finish <= 10^15"
    assert 1 <= limit <= 9, "1 <= limit <= 9"
    assert 1 <= len(s) <= len(str(finish)), "1 <= s.length <= floor(log10(finish)) + 1"
    assert all(c in "0123456789" for c in s), "s only consists of numeric digits"
    assert all(int(c) <= limit for c in s), "digits of s are at most limit"
    assert s[0] != "0", "s does not have leading zeros"
