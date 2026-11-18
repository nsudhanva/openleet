"""X of a Kind in a Deck of Cards: a list of card values."""


def check(deck: list[int]) -> None:
    assert 1 <= len(deck) <= 10**4, "1 <= deck.length <= 10^4"
    assert all(0 <= v < 10**4 for v in deck), "0 <= deck[i] < 10^4"
