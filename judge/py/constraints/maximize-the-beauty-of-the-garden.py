"""Maximize the Beauty of the Garden: a list of flower beauty values."""


def check(flowers: list[int]) -> None:
    assert 2 <= len(flowers) <= 10**5, "2 <= flowers.length <= 10^5"
    assert all(-(10**4) <= v <= 10**4 for v in flowers), "-10^4 <= flowers[i] <= 10^4"
    assert len(set(flowers)) < len(flowers), "a valid garden can be created (some beauty repeats)"
