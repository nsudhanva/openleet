"""Maximum Total Subarray Value I: an array of non-negative ints and a count k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
