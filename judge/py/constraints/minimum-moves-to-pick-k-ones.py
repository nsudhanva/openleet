"""Minimum Moves to Pick K Ones: a binary array, k ones to pick and maxChanges."""


def check(nums: list[int], k: int, maxChanges: int) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= n <= 10^5"
    assert all(v in (0, 1) for v in nums), "0 <= nums[i] <= 1"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
    assert 0 <= maxChanges <= 10**5, "0 <= maxChanges <= 10^5"
    assert maxChanges + sum(nums) >= k, "maxChanges + sum(nums) >= k"
