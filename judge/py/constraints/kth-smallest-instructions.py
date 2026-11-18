"""Kth Smallest Instructions: a [row, column] destination and k."""

from math import comb


def check(destination: list[int], k: int) -> None:
    assert len(destination) == 2, "destination.length == 2"
    row, column = destination
    assert 1 <= row <= 15 and 1 <= column <= 15, "1 <= row, column <= 15"
    assert 1 <= k <= comb(row + column, row), "1 <= k <= nCr(row + column, row)"
