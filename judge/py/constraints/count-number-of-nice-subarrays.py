"""Count Number of Nice Subarrays: an integer array and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 50000, "1 <= nums.length <= 50000"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
