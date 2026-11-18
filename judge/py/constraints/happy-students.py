"""Happy Students: an array of thresholds below its length."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v < n for v in nums), "0 <= nums[i] < nums.length"
