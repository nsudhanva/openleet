"""Number of Distinct Averages: an even-length array of small non-negative integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert len(nums) % 2 == 0, "nums.length is even"
    assert all(0 <= v <= 100 for v in nums), "0 <= nums[i] <= 100"
