"""Number of Subarrays That Match a Pattern I: an integer array and a pattern of -1, 0, 1."""


def check(nums: list[int], pattern: list[int]) -> None:
    assert isinstance(nums, list) and isinstance(pattern, list), "lists"
    n, m = len(nums), len(pattern)
    assert 2 <= n <= 100, "2 <= n == nums.length <= 100"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= m < n, "1 <= m == pattern.length < n"
    assert all(-1 <= v <= 1 for v in pattern), "-1 <= pattern[i] <= 1"
