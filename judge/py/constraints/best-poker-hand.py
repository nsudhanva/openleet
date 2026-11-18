"""Best Poker Hand: five card ranks and suits."""


def check(ranks: list[int], suits: list[str]) -> None:
    assert len(ranks) == len(suits) == 5, "ranks.length == suits.length == 5"
    assert all(isinstance(r, int) and 1 <= r <= 13 for r in ranks), "1 <= ranks[i] <= 13"
    assert all(isinstance(s, str) and len(s) == 1 and "a" <= s <= "d" for s in suits), (
        "'a' <= suits[i] <= 'd'"
    )
    assert len(set(zip(ranks, suits, strict=True))) == 5, "no two cards have the same rank and suit"
