"""Most Frequent Even Element: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2000, "1 <= nums.length <= 2000"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
