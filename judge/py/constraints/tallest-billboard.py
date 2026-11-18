"""Tallest Billboard: a list of rod lengths."""


def check(rods: list[int]) -> None:
    assert 1 <= len(rods) <= 20, "1 <= rods.length <= 20"
    assert all(1 <= r <= 1000 for r in rods), "1 <= rods[i] <= 1000"
    assert sum(rods) <= 5000, "sum(rods[i]) <= 5000"
