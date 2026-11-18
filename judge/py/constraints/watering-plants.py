"""Watering Plants: plant water needs and a can capacity."""


def check(plants: list[int], capacity: int) -> None:
    assert 1 <= len(plants) <= 1000, "1 <= n <= 1000"
    assert all(1 <= p <= 10**6 for p in plants), "1 <= plants[i] <= 10^6"
    assert max(plants) <= capacity <= 10**9, "max(plants[i]) <= capacity <= 10^9"
