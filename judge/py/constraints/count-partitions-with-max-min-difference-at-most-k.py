"""Count Partitions With Max-Min Difference at Most K: an integer array and k."""


def check(nums: list[int], k: int) -> None:
    assert 2 <= len(nums) <= 5 * 10**4, "2 <= nums.length <= 5 * 10^4"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 0 <= k <= 10**9, "0 <= k <= 10^9"
