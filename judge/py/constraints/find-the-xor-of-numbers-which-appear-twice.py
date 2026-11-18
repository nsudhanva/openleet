"""Find the XOR of Numbers Which Appear Twice: an array where each number appears once or twice."""

from collections import Counter


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 50, "1 <= nums.length <= 50"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
    assert all(c <= 2 for c in Counter(nums).values()), (
        "each number in nums appears either once or twice"
    )
