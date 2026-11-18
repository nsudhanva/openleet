"""Maximum Product of Three Elements After One Replacement: an integer array."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= nums.length <= 10^5"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
