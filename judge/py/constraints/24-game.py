"""24 Game: four cards."""


def check(cards: list[int]) -> None:
    assert len(cards) == 4, "cards.length == 4"
    assert all(1 <= c <= 9 for c in cards), "1 <= cards[i] <= 9"
