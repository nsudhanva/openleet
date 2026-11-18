"""Optimal Division: a list of 1 to 10 integers with a unique optimal division."""

from fractions import Fraction
from typing import cast


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 10, "1 <= nums.length <= 10"
    assert all(2 <= v <= 1000 for v in nums), "2 <= nums[i] <= 1000"
    # best[i][j] = (max value, ways to reach it, min value, ways to reach it) over all
    # parenthesisations of nums[i..j]
    best: dict[tuple[int, int], tuple[Fraction, int, Fraction, int]] = {}
    for i, v in enumerate(nums):
        best[i, i] = (Fraction(v), 1, Fraction(v), 1)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            hi, hi_ways, lo, lo_ways = None, 0, None, 0
            for k in range(i, j):
                lmax, lmax_w, lmin, lmin_w = best[i, k]
                rmax, rmax_w, rmin, rmin_w = best[k + 1, j]
                top, top_w = lmax / rmin, lmax_w * rmin_w
                bottom, bottom_w = lmin / rmax, lmin_w * rmax_w
                if hi is None or top > hi:
                    hi, hi_ways = top, top_w
                elif top == hi:
                    hi_ways += top_w
                if lo is None or bottom < lo:
                    lo, lo_ways = bottom, bottom_w
                elif bottom == lo:
                    lo_ways += bottom_w
            best[i, j] = (cast(Fraction, hi), hi_ways, cast(Fraction, lo), lo_ways)
    assert best[0, n - 1][1] == 1, "there is only one optimal division for the given input"
