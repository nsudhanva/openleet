"""Rearrange Array Elements by Sign: equal counts of positive and negative integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 2 * 10**5, "2 <= nums.length <= 2 * 10^5"
    assert len(nums) % 2 == 0, "nums.length is even"
    assert all(1 <= abs(v) <= 10**5 for v in nums), "1 <= |nums[i]| <= 10^5"
    assert 2 * sum(v > 0 for v in nums) == len(nums), (
        "equal number of positive and negative integers"
    )
