"""Number of Substrings Containing All Three Characters: a string over a, b, c."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 3 <= len(s) <= 5 * 10**4, "3 <= s.length <= 5 x 10^4"
    assert set(s) <= {"a", "b", "c"}, "s only consists of 'a', 'b' or 'c'"
