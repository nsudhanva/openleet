"""Merge Triplets to Form Target Triplet: a list of integer triplets and a target triplet."""


def check(triplets: list[list[int]], target: list[int]) -> None:
    assert 1 <= len(triplets) <= 10**5, "1 <= triplets.length <= 10^5"
    assert all(len(t) == 3 for t in triplets), "triplets[i].length == 3"
    assert len(target) == 3, "target.length == 3"
    assert all(1 <= v <= 1000 for t in triplets for v in t), "1 <= ai, bi, ci <= 1000"
    assert all(1 <= v <= 1000 for v in target), "1 <= x, y, z <= 1000"
