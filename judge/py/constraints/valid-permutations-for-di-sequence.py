"""Valid Permutations for DI Sequence: a string of 'D' and 'I'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 200, "1 <= n <= 200"
    assert all(c in "DI" for c in s), "s[i] is either 'I' or 'D'"
