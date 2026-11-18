"""Repeated DNA Sequences: a string over A, C, G, T."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "ACGT" for c in s), "s[i] is either 'A', 'C', 'G', or 'T'"
