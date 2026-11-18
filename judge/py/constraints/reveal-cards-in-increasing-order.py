"""Reveal Cards In Increasing Order: a deck of unique positive integers."""


def check(deck: list[int]) -> None:
    assert 1 <= len(deck) <= 1000, "1 <= deck.length <= 1000"
    assert all(1 <= v <= 10**6 for v in deck), "1 <= deck[i] <= 10^6"
    assert len(set(deck)) == len(deck), "all the values of deck are unique"
