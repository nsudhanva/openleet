"""Erect the Fence: distinct tree positions on a grid."""


def check(trees: list[list[int]]) -> None:
    assert 1 <= len(trees) <= 3000, "1 <= trees.length <= 3000"
    assert all(isinstance(p, list) and len(p) == 2 for p in trees), "trees[i].length == 2"
    assert all(isinstance(v, int) and 0 <= v <= 100 for p in trees for v in p), "0 <= xi, yi <= 100"
    assert len({tuple(p) for p in trees}) == len(trees), "all the given positions are unique"
