"""Number of Ways to Split Array: an integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
