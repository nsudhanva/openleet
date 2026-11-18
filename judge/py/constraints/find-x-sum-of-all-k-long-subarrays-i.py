"""Find X-Sum of All K-Long Subarrays I: an array of small positive ints with k and x."""


def check(nums: list[int], k: int, x: int) -> None:
    assert 1 <= len(nums) <= 50, "1 <= n == nums.length <= 50"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
    assert 1 <= x <= k <= len(nums), "1 <= x <= k <= nums.length"
