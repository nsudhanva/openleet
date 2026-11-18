"""Bag of Tokens: token values and an initial power."""


def check(tokens: list[int], power: int) -> None:
    assert 0 <= len(tokens) <= 1000, "0 <= tokens.length <= 1000"
    assert all(0 <= v < 10**4 for v in tokens), "0 <= tokens[i] < 10^4"
    assert 0 <= power < 10**4, "0 <= power < 10^4"
