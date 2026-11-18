"""Maximize Win From Two Segments: sorted prize positions and segment length k."""

from itertools import pairwise


def check(prizePositions: list[int], k: int) -> None:
    assert 1 <= len(prizePositions) <= 10**5, "1 <= prizePositions.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in prizePositions), "1 <= prizePositions[i] <= 10^9"
    assert 0 <= k <= 10**9, "0 <= k <= 10^9"
    assert all(a <= b for a, b in pairwise(prizePositions)), (
        "prizePositions is sorted in non-decreasing order"
    )
