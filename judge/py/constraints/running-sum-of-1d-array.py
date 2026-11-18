"""Running Sum of 1d Array: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(-(10**6) <= v <= 10**6 for v in nums), "-10^6 <= nums[i] <= 10^6"
