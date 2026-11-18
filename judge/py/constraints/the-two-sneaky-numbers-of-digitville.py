"""The Two Sneaky Numbers of Digitville: n + 2 numbers in [0, n) with exactly two repeats."""

from collections import Counter


def check(nums: list[int]) -> None:
    n = len(nums) - 2
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert all(0 <= x < n for x in nums), "0 <= nums[i] < n"
    counts = Counter(nums)
    assert sum(c == 2 for c in counts.values()) == 2, "nums contains exactly two repeated elements"
    assert all(c <= 2 for c in counts.values()), "no element is repeated more than once"
