"""Find the Power of K-Size Subarrays I: an array nums and a window size k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 500, "1 <= n == nums.length <= 500"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert 1 <= k <= n, "1 <= k <= n"
