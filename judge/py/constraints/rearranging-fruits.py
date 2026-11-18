"""Rearranging Fruits: two equal-length baskets of fruit costs."""


def check(basket1: list[int], basket2: list[int]) -> None:
    assert len(basket1) == len(basket2), "basket1.length == basket2.length"
    assert 1 <= len(basket1) <= 10**5, "1 <= basket1.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in basket1 + basket2), "1 <= basket1[i], basket2[i] <= 10^9"
