"""Sum of Imbalance Numbers of All Subarrays: values in 1..nums.length."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= x <= len(nums) for x in nums), "1 <= nums[i] <= nums.length"
