"""Special Array With X Elements Greater Than or Equal X: a list of non-negative integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(isinstance(v, int) and 0 <= v <= 1000 for v in nums), "0 <= nums[i] <= 1000"
