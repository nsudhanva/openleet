"""Construct the Rectangle: a target area."""


def check(area: int) -> None:
    assert isinstance(area, int), "area is an integer"
    assert 1 <= area <= 10**7, "1 <= area <= 10^7"
