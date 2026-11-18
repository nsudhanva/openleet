"""Maximum Median Sum of Subsequences of Size 3: an integer array whose length is a
multiple of 3."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 5 * 10**5, "1 <= nums.length <= 5 * 10^5"
    assert len(nums) % 3 == 0, "nums.length % 3 == 0"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
