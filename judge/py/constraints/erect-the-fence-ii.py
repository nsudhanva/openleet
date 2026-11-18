"""Erect the Fence II: tree positions on a grid."""


def check(trees: list[list[int]]) -> None:
    assert 1 <= len(trees) <= 3000, "1 <= trees.length <= 3000"
    assert all(isinstance(p, list) and len(p) == 2 for p in trees), "trees[i].length == 2"
    assert all(isinstance(v, int) and 0 <= v <= 3000 for p in trees for v in p), (
        "trees is List[List[int]] with 0 <= xi, yi <= 3000"
    )
