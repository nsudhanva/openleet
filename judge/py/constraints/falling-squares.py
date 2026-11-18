"""Falling Squares: a list of [left, sideLength] squares."""


def check(positions: list[list[int]]) -> None:
    assert 1 <= len(positions) <= 1000, "1 <= positions.length <= 1000"
    assert all(len(p) == 2 for p in positions), "positions[i].length == 2"
    assert all(1 <= left <= 10**8 for left, _ in positions), "1 <= lefti <= 10^8"
    assert all(1 <= side <= 10**6 for _, side in positions), "1 <= sideLengthi <= 10^6"
