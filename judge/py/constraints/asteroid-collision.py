"""Asteroid Collision: non-zero integers (size and direction)."""


def check(asteroids: list[int]) -> None:
    assert 2 <= len(asteroids) <= 10**4, "2 <= asteroids.length <= 10^4"
    assert all(-1000 <= v <= 1000 for v in asteroids), "-1000 <= asteroids[i] <= 1000"
    assert all(v != 0 for v in asteroids), "asteroids[i] != 0"
