"""Check If String Is Transformable With Substring Sort Operations: two digit strings."""


def check(s: str, t: str) -> None:
    assert len(s) == len(t), "s.length == t.length"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert (s + t).isascii() and (s + t).isdigit(), "s and t consist of only digits"
