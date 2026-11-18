"""Count Number of Special Subsequences: an array of 0s, 1s and 2s."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 2 for v in nums), "0 <= nums[i] <= 2"
