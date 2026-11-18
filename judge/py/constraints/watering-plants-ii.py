"""Watering Plants II: plant water needs and two can capacities."""


def check(plants: list[int], capacityA: int, capacityB: int) -> None:
    assert 1 <= len(plants) <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= p <= 10**6 for p in plants), "1 <= plants[i] <= 10^6"
    assert max(plants) <= capacityA <= 10**9, "max(plants[i]) <= capacityA <= 10^9"
    assert max(plants) <= capacityB <= 10**9, "max(plants[i]) <= capacityB <= 10^9"
