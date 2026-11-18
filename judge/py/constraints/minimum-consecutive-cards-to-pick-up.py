"""Minimum Consecutive Cards to Pick Up: a list of card values."""


def check(cards: list[int]) -> None:
    assert 1 <= len(cards) <= 10**5, "1 <= cards.length <= 10^5"
    assert all(0 <= v <= 10**6 for v in cards), "0 <= cards[i] <= 10^6"
