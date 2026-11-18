"""Single Number: integers where one appears once and the rest twice."""

from collections import Counter


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 3 * 10**4, "1 <= nums.length <= 3 * 10^4"
    assert all(-3 * 10**4 <= v <= 3 * 10**4 for v in nums), "-3 * 10^4 <= nums[i] <= 3 * 10^4"
    counts = Counter(nums)
    assert sum(c == 1 for c in counts.values()) == 1, "exactly one element appears once"
    assert all(c in (1, 2) for c in counts.values()), "every other element appears twice"
