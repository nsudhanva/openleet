"""Target Sum: non-negative integers and a target."""


def check(nums: list[int], target: int) -> None:
    assert 1 <= len(nums) <= 20, "1 <= nums.length <= 20"
    assert all(0 <= x <= 1000 for x in nums), "0 <= nums[i] <= 1000"
    assert 0 <= sum(nums) <= 1000, "0 <= sum(nums[i]) <= 1000"
    assert -1000 <= target <= 1000, "-1000 <= target <= 1000"
