"""Maximum Height by Stacking Cuboids: n cuboids given as [width, length, height]."""


def check(cuboids: list[list[int]]) -> None:
    assert 1 <= len(cuboids) <= 100, "1 <= n <= 100"
    assert all(len(c) == 3 for c in cuboids), "each cuboid has width, length and height"
    assert all(1 <= d <= 100 for c in cuboids for d in c), "1 <= widthi, lengthi, heighti <= 100"
