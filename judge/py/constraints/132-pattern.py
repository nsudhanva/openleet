"""132 Pattern: a list of integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2 * 10**5, "1 <= n <= 2 * 10^5"
    assert all(-(10**9) <= x <= 10**9 for x in nums), "-10^9 <= nums[i] <= 10^9"
