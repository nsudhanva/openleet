"""Minimum Cost of Buying Candies With Discount: a list of candy prices."""


def check(cost: list[int]) -> None:
    assert 1 <= len(cost) <= 100, "1 <= cost.length <= 100"
    assert all(1 <= c <= 100 for c in cost), "1 <= cost[i] <= 100"
