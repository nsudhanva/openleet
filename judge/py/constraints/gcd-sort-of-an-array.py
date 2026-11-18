"""GCD Sort of an Array: an array of integers at least 2."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 3 * 10**4, "1 <= nums.length <= 3 * 10^4"
    assert all(2 <= v <= 10**5 for v in nums), "2 <= nums[i] <= 10^5"
