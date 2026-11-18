"""Maximum Product of Three Numbers: an integer array."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**4, "3 <= nums.length <= 10^4"
    assert all(-1000 <= v <= 1000 for v in nums), "-1000 <= nums[i] <= 1000"
