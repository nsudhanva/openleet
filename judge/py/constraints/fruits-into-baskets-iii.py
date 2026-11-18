"""Fruits Into Baskets III: fruit quantities and basket capacities of equal length."""


def check(fruits: list[int], baskets: list[int]) -> None:
    n = len(fruits)
    assert len(baskets) == n, "n == fruits.length == baskets.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= 10**9 for v in fruits), "1 <= fruits[i] <= 10^9"
    assert all(1 <= v <= 10**9 for v in baskets), "1 <= baskets[i] <= 10^9"
