"""Maximum Sum of 3 Non-Overlapping Subarrays: a positive integer array and a window size k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 2 * 10**4, "1 <= nums.length <= 2 * 10^4"
    assert all(1 <= v < 2**16 for v in nums), "1 <= nums[i] < 2^16"
    assert 1 <= k <= len(nums) // 3, "1 <= k <= floor(nums.length / 3)"
