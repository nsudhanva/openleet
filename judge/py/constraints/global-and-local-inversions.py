"""Global and Local Inversions: a permutation of 0..n-1."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= v < n for v in nums), "0 <= nums[i] < n"
    assert len(set(nums)) == n, "all the integers of nums are unique"
    assert sorted(nums) == list(range(n)), "nums is a permutation of [0, n - 1]"
