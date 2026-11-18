"""Circle and Rectangle Overlapping: a circle and an axis-aligned rectangle."""


def check(radius: int, xCenter: int, yCenter: int, x1: int, y1: int, x2: int, y2: int) -> None:
    assert 1 <= radius <= 2000, "1 <= radius <= 2000"
    assert -(10**4) <= xCenter <= 10**4, "-10^4 <= xCenter <= 10^4"
    assert -(10**4) <= yCenter <= 10**4, "-10^4 <= yCenter <= 10^4"
    assert -(10**4) <= x1 < x2 <= 10**4, "-10^4 <= x1 < x2 <= 10^4"
    assert -(10**4) <= y1 < y2 <= 10**4, "-10^4 <= y1 < y2 <= 10^4"
