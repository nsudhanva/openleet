"""Maximum Total Damage With Spell Casting: an array of spell damages."""


def check(power: list[int]) -> None:
    assert 1 <= len(power) <= 10**5, "1 <= power.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in power), "1 <= power[i] <= 10^9"
