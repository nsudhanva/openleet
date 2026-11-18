"""Array Nesting: a permutation of 0..n-1."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v < n for v in nums), "0 <= nums[i] < nums.length"
    assert len(set(nums)) == n, "all the values of nums are unique"
