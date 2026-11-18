"""Alphabet Board Path: a lowercase target string."""


def check(target: str) -> None:
    assert 1 <= len(target) <= 100, "1 <= target.length <= 100"
    assert all("a" <= c <= "z" for c in target), "target consists only of English lowercase letters"
