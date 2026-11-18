"""Fruit Into Baskets: an array of fruit types."""


def check(fruits: list[int]) -> None:
    assert 1 <= len(fruits) <= 10**5, "1 <= fruits.length <= 10^5"
    assert all(0 <= f < len(fruits) for f in fruits), "0 <= fruits[i] < fruits.length"
