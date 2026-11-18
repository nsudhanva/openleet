"""Largest Substring Between Two Equal Characters: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 300, "1 <= s.length <= 300"
    assert all("a" <= c <= "z" and len(c) == 1 for c in s), (
        "s contains only lowercase English letters"
    )
