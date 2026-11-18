"""Widest Possible Fence: a list of plank heights."""


def check(planks: list[int]) -> None:
    assert 1 <= len(planks) <= 1000, "1 <= planks.length <= 1000"
    assert all(1 <= v <= 10**9 for v in planks), "1 <= planks[i] <= 10^9"
