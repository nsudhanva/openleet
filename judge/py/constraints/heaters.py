"""Heaters: positions of houses and heaters on a line."""


def check(houses: list[int], heaters: list[int]) -> None:
    assert 1 <= len(houses) <= 3 * 10**4, "1 <= houses.length <= 3 * 10^4"
    assert 1 <= len(heaters) <= 3 * 10**4, "1 <= heaters.length <= 3 * 10^4"
    assert all(1 <= h <= 10**9 for h in houses), "1 <= houses[i] <= 10^9"
    assert all(1 <= h <= 10**9 for h in heaters), "1 <= heaters[i] <= 10^9"
