"""Maximum Erasure Value: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
