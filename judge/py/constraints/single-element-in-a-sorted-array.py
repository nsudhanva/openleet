"""Single Element in a Sorted Array: a sorted array where one value appears once, the rest twice."""

from collections import Counter


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
    assert all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)), "nums is sorted"
    counts = Counter(nums)
    assert sum(c == 1 for c in counts.values()) == 1, "exactly one element appears once"
    assert all(c in (1, 2) for c in counts.values()), "every other element appears exactly twice"
