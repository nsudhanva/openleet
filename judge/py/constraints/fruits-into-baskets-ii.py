"""Fruits Into Baskets II: fruit quantities and basket capacities of equal length."""


def check(fruits: list[int], baskets: list[int]) -> None:
    n = len(fruits)
    assert len(baskets) == n, "n == fruits.length == baskets.length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(1 <= v <= 1000 for v in fruits), "1 <= fruits[i] <= 1000"
    assert all(1 <= v <= 1000 for v in baskets), "1 <= baskets[i] <= 1000"
