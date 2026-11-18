"""Find Closest Person: positions x, y and z on a number line."""


def check(x: int, y: int, z: int) -> None:
    assert all(1 <= v <= 100 for v in (x, y, z)), "1 <= x, y, z <= 100"
