"""Count Subarrays With Median K: a permutation of 1..n and k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= n for v in nums), "1 <= nums[i] <= n"
    assert len(set(nums)) == n, "the integers in nums are distinct"
    assert 1 <= k <= n, "1 <= k <= n"
