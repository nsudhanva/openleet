"""Minimum Amount of Damage Dealt to Bob: attack power and per-enemy damage and health."""


def check(power: int, damage: list[int], health: list[int]) -> None:
    assert 1 <= power <= 10**4, "1 <= power <= 10^4"
    assert 1 <= len(damage) <= 10**5, "1 <= n <= 10^5"
    assert len(damage) == len(health), "n == damage.length == health.length"
    assert all(1 <= v <= 10**4 for v in damage), "1 <= damage[i] <= 10^4"
    assert all(1 <= v <= 10**4 for v in health), "1 <= health[i] <= 10^4"
