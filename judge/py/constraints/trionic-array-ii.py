"""Trionic Array II: an integer array containing a trionic subarray."""

from itertools import pairwise


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 4 <= n <= 10**5, "4 <= n <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    # run-length encode the signs of consecutive differences; 0 breaks adjacency
    runs: list[int] = []
    for a, b in pairwise(nums):
        s = (b > a) - (b < a)
        if s == 0:
            runs.append(0)
        elif not runs or runs[-1] != s:
            runs.append(s)
    assert any(runs[i : i + 3] == [1, -1, 1] for i in range(len(runs))), (
        "at least one trionic subarray exists"
    )
