"""Find the Most Competitive Subsequence: an array of non-negative integers and a length k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
