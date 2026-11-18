"""Max Pair Sum in an Array: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
