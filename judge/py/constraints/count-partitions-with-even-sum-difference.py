"""Count Partitions with Even Sum Difference: an integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 100, "2 <= n == nums.length <= 100"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
