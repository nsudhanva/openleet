"""Find X-Sum of All K-Long Subarrays II: an array of positive ints with k and x."""


def check(nums: list[int], k: int, x: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= n == nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= x <= k <= len(nums), "1 <= x <= k <= nums.length"
