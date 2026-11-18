"""3Sum Closest: a list of integers and a target."""


def check(nums: list[int], target: int) -> None:
    assert 3 <= len(nums) <= 500, "3 <= nums.length <= 500"
    assert all(-1000 <= x <= 1000 for x in nums), "-1000 <= nums[i] <= 1000"
    assert -(10**4) <= target <= 10**4, "-10^4 <= target <= 10^4"
