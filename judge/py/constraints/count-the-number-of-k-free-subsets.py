"""Count the Number of K-Free Subsets: an array of positive integers and k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 50, "1 <= nums.length <= 50"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
    assert 1 <= k <= 1000, "1 <= k <= 1000"
