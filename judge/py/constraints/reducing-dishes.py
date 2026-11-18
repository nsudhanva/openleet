"""Reducing Dishes: a list of dish satisfaction levels."""


def check(satisfaction: list[int]) -> None:
    assert 1 <= len(satisfaction) <= 500, "1 <= n <= 500"
    assert all(-1000 <= v <= 1000 for v in satisfaction), "-1000 <= satisfaction[i] <= 1000"
