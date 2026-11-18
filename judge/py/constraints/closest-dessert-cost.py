"""Closest Dessert Cost: base costs, topping costs and a target."""


def check(baseCosts: list[int], toppingCosts: list[int], target: int) -> None:
    assert 1 <= len(baseCosts) <= 10, "1 <= n <= 10"
    assert 1 <= len(toppingCosts) <= 10, "1 <= m <= 10"
    assert all(1 <= v <= 10**4 for v in baseCosts), "1 <= baseCosts[i] <= 10^4"
    assert all(1 <= v <= 10**4 for v in toppingCosts), "1 <= toppingCosts[i] <= 10^4"
    assert 1 <= target <= 10**4, "1 <= target <= 10^4"
