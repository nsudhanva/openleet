"""Water and Jug Problem: two jug capacities and a target volume."""


def check(x: int, y: int, target: int) -> None:
    assert 1 <= x <= 10**3, "1 <= x <= 10^3"
    assert 1 <= y <= 10**3, "1 <= y <= 10^3"
    assert 1 <= target <= 10**3, "1 <= target <= 10^3"
