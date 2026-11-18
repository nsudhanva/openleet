"""Sum of Total Strength of Wizards: an array of strengths."""


def check(strength: list[int]) -> None:
    assert 1 <= len(strength) <= 100000, "1 <= strength.length <= 100000"
    assert all(1 <= v <= 1000000000 for v in strength), "1 <= strength[i] <= 10^9"
