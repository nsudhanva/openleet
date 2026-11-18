"""Count the Number of Square-Free Subsets: an array of integers 1..30."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 30 for v in nums), "1 <= nums[i] <= 30"
