"""Frog Jump II: stone positions in strictly increasing order starting at 0."""

from itertools import pairwise


def check(stones: list[int]) -> None:
    assert 2 <= len(stones) <= 10**5, "2 <= stones.length <= 10^5"
    assert all(0 <= s <= 10**9 for s in stones), "0 <= stones[i] <= 10^9"
    assert stones[0] == 0, "stones[0] == 0"
    assert all(a < b for a, b in pairwise(stones)), "stones is strictly increasing"
