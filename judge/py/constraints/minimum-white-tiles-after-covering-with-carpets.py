"""Minimum White Tiles After Covering With Carpets: a binary floor string, carpets, length."""


def check(floor: str, numCarpets: int, carpetLen: int) -> None:
    assert 1 <= carpetLen <= len(floor) <= 1000, "1 <= carpetLen <= floor.length <= 1000"
    assert set(floor) <= {"0", "1"}, "floor[i] is either '0' or '1'"
    assert 1 <= numCarpets <= 1000, "1 <= numCarpets <= 1000"
