"""4Sum: a list of integers and a target."""


def check(nums: list[int], target: int) -> None:
    assert 1 <= len(nums) <= 200, "1 <= nums.length <= 200"
    assert all(-(10**9) <= x <= 10**9 for x in nums), "-10^9 <= nums[i] <= 10^9"
    assert -(10**9) <= target <= 10**9, "-10^9 <= target <= 10^9"
