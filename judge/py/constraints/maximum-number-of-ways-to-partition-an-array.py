"""Maximum Number of Ways to Partition an Array: an integer array and a replacement value k."""


def check(nums: list[int], k: int) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= n <= 10^5"
    assert -(10**5) <= k <= 10**5, "-10^5 <= k <= 10^5"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
