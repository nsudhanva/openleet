"""Form Largest Integer With Digits That Add up to Target: nine digit costs and a target."""


def check(cost: list[int], target: int) -> None:
    assert len(cost) == 9, "cost.length == 9"
    assert all(1 <= c <= 5000 for c in cost), "1 <= cost[i] <= 5000"
    assert 1 <= target <= 5000, "1 <= target <= 5000"
