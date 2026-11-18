"""Destroying Asteroids: a planet mass and asteroid masses."""


def check(mass: int, asteroids: list[int]) -> None:
    assert 1 <= mass <= 10**5, "1 <= mass <= 10^5"
    assert 1 <= len(asteroids) <= 10**5, "1 <= asteroids.length <= 10^5"
    assert all(1 <= a <= 10**5 for a in asteroids), "1 <= asteroids[i] <= 10^5"
