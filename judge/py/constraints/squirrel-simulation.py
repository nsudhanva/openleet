"""Squirrel Simulation: a grid size, tree and squirrel cells and nut cells."""


def check(
    height: int, width: int, tree: list[int], squirrel: list[int], nuts: list[list[int]]
) -> None:
    assert 1 <= height <= 100 and 1 <= width <= 100, "1 <= height, width <= 100"
    assert len(tree) == 2, "tree.length == 2"
    assert len(squirrel) == 2, "squirrel.length == 2"
    assert 1 <= len(nuts) <= 5000, "1 <= nuts.length <= 5000"
    assert all(len(n) == 2 for n in nuts), "nuts[i].length == 2"
    assert all(0 <= p[0] <= height for p in [tree, squirrel, *nuts]), (
        "0 <= treer, squirrelr, nutir <= height"
    )
    assert all(0 <= p[1] <= width for p in [tree, squirrel, *nuts]), (
        "0 <= treec, squirrelc, nutic <= width"
    )
