"""Sort an Array: a list of integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 5 * 10**4, "1 <= nums.length <= 5 * 10^4"
    assert all(-5 * 10**4 <= v <= 5 * 10**4 for v in nums), "-5 * 10^4 <= nums[i] <= 5 * 10^4"
