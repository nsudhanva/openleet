"""Painting the Walls: the cost and time of painting each wall."""


def check(cost: list[int], time: list[int]) -> None:
    assert isinstance(cost, list) and isinstance(time, list), "cost and time are lists"
    assert 1 <= len(cost) <= 500, "1 <= cost.length <= 500"
    assert len(cost) == len(time), "cost.length == time.length"
    assert all(1 <= c <= 10**6 for c in cost), "1 <= cost[i] <= 10^6"
    assert all(1 <= t <= 500 for t in time), "1 <= time[i] <= 500"
