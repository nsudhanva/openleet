"""Find the Minimum Amount of Time to Brew Potions: wizard skills and potion manas."""


def check(skill: list[int], mana: list[int]) -> None:
    assert 1 <= len(skill) <= 5000, "1 <= n <= 5000"
    assert 1 <= len(mana) <= 5000, "1 <= m <= 5000"
    assert all(1 <= v <= 5000 for v in skill), "1 <= skill[i] <= 5000"
    assert all(1 <= v <= 5000 for v in mana), "1 <= mana[i] <= 5000"
