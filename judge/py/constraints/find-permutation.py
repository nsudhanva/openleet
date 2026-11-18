"""Find Permutation: a string of 'I' and 'D'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "ID" for c in s), "s[i] is either 'I' or 'D'"
