"""Single Number III: integers where two appear once and the rest twice."""

from collections import Counter


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 3 * 10**4, "2 <= nums.length <= 3 * 10^4"
    assert all(-(2**31) <= v <= 2**31 - 1 for v in nums), "-2^31 <= nums[i] <= 2^31 - 1"
    counts = Counter(nums)
    assert sum(c == 1 for c in counts.values()) == 2, "exactly two integers appear once"
    assert all(c in (1, 2) for c in counts.values()), "every other integer appears twice"
