"""House Robber II: money in a circle of houses."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(0 <= x <= 1000 for x in nums), "0 <= nums[i] <= 1000"
