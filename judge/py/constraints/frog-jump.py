"""Frog Jump: stone positions in strictly increasing order starting at 0."""

from itertools import pairwise


def check(stones: list[int]) -> None:
    assert 2 <= len(stones) <= 2000, "2 <= stones.length <= 2000"
    assert all(0 <= s <= 2**31 - 1 for s in stones), "0 <= stones[i] <= 2^31 - 1"
    assert stones[0] == 0, "stones[0] == 0"
    assert all(a < b for a, b in pairwise(stones)), "stones is strictly increasing"
