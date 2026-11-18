"""Minimum Hours of Training to Win a Competition: initial stats and opponents."""


def check(
    initialEnergy: int, initialExperience: int, energy: list[int], experience: list[int]
) -> None:
    n = len(energy)
    assert len(experience) == n, "n == energy.length == experience.length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert 1 <= initialEnergy <= 100, "1 <= initialEnergy <= 100"
    assert 1 <= initialExperience <= 100, "1 <= initialExperience <= 100"
    assert all(1 <= x <= 100 for x in energy), "1 <= energy[i] <= 100"
    assert all(1 <= x <= 100 for x in experience), "1 <= experience[i] <= 100"
