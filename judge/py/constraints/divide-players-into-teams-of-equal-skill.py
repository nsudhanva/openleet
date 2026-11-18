"""Divide Players Into Teams of Equal Skill: an even-length list of skills."""


def check(skill: list[int]) -> None:
    assert 2 <= len(skill) <= 10**5, "2 <= skill.length <= 10^5"
    assert len(skill) % 2 == 0, "skill.length is even"
    assert all(1 <= v <= 1000 for v in skill), "1 <= skill[i] <= 1000"
