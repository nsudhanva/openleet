"""Dice Roll Simulation: roll count and consecutive-roll limits of a 6-sided die."""


def check(n: int, rollMax: list[int]) -> None:
    assert 1 <= n <= 5000, "1 <= n <= 5000"
    assert len(rollMax) == 6, "rollMax.length == 6"
    assert all(1 <= v <= 15 for v in rollMax), "1 <= rollMax[i] <= 15"
