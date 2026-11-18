"""Min Cost Climbing Stairs: an array of step costs."""


def check(cost: list[int]) -> None:
    assert 2 <= len(cost) <= 1000, "2 <= cost.length <= 1000"
    assert all(0 <= v <= 999 for v in cost), "0 <= cost[i] <= 999"
