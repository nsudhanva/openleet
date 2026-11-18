"""Find the K-Sum of an Array: an integer array and k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert 1 <= k <= min(2000, 2**n), "1 <= k <= min(2000, 2^n)"
