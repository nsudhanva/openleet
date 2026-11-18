"""Minimum Domino Rotations For Equal Row: tops and bottoms of dominoes with values 1..6."""


def check(tops: list[int], bottoms: list[int]) -> None:
    assert 2 <= len(tops) <= 2 * 10**4, "2 <= tops.length <= 2 * 10^4"
    assert len(bottoms) == len(tops), "bottoms.length == tops.length"
    assert all(1 <= x <= 6 for x in tops), "1 <= tops[i] <= 6"
    assert all(1 <= x <= 6 for x in bottoms), "1 <= bottoms[i] <= 6"
