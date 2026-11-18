"""Maximum Binary Tree: an array of unique integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(0 <= v <= 1000 for v in nums), "0 <= nums[i] <= 1000"
    assert len(set(nums)) == len(nums), "all integers in nums are unique"
