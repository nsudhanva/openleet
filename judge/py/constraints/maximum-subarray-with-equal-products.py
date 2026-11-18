"""Maximum Subarray With Equal Products: a short array of integers 1..10."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert all(1 <= v <= 10 for v in nums), "1 <= nums[i] <= 10"
