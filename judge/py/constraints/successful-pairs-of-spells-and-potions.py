"""Successful Pairs of Spells and Potions: spell strengths, potion strengths and a threshold."""


def check(spells: list[int], potions: list[int], success: int) -> None:
    assert 1 <= len(spells) <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(potions) <= 10**5, "1 <= m <= 10^5"
    assert all(1 <= x <= 10**5 for x in spells), "1 <= spells[i] <= 10^5"
    assert all(1 <= x <= 10**5 for x in potions), "1 <= potions[i] <= 10^5"
    assert 1 <= success <= 10**10, "1 <= success <= 10^10"
