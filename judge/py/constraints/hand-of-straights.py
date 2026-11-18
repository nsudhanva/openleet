"""Hand of Straights: a hand of cards and a group size."""


def check(hand: list[int], groupSize: int) -> None:
    assert 1 <= len(hand) <= 10**4, "1 <= hand.length <= 10^4"
    assert all(0 <= c <= 10**9 for c in hand), "0 <= hand[i] <= 10^9"
    assert 1 <= groupSize <= len(hand), "1 <= groupSize <= hand.length"
