"""Find the Longest Equal Subarray: an array of values up to its length and a deletion budget."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= n for v in nums), "1 <= nums[i] <= nums.length"
    assert 0 <= k <= n, "0 <= k <= nums.length"
