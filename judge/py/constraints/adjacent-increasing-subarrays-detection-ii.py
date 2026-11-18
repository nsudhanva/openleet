"""Adjacent Increasing Subarrays Detection II: a list of integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 2 * 10**5, "2 <= nums.length <= 2 * 10^5"
    assert all(-(10**9) <= x <= 10**9 for x in nums), "-10^9 <= nums[i] <= 10^9"
