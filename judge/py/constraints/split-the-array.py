"""Split the Array: an even-length array of small positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert len(nums) % 2 == 0, "nums.length % 2 == 0"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
