"""3Sum: a list of integers."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 3000, "3 <= nums.length <= 3000"
    assert all(-(10**5) <= x <= 10**5 for x in nums), "-10^5 <= nums[i] <= 10^5"
