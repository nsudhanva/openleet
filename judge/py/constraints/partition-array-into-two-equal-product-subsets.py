"""Partition Array into Two Equal Product Subsets: distinct integers and a target product."""


def check(nums: list[int], target: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 3 <= len(nums) <= 12, "3 <= nums.length <= 12"
    assert isinstance(target, int) and 1 <= target <= 10**15, "1 <= target <= 10^15"
    assert all(isinstance(v, int) and 1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert len(set(nums)) == len(nums), "All elements of nums are distinct"
