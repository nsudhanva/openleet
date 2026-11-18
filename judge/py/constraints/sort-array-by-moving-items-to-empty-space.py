"""Sort Array by Moving Items to Empty Space: a permutation of 0..n-1."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(isinstance(v, int) and 0 <= v < n for v in nums), "0 <= nums[i] < n"
    assert len(set(nums)) == n, "all the values of nums are unique"
