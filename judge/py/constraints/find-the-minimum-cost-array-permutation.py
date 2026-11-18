"""Find the Minimum Cost Array Permutation: a permutation of 0..n-1."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 2 <= n <= 14, "2 <= n == nums.length <= 14"
    assert sorted(nums) == list(range(n)), "nums is a permutation of [0, 1, 2, ..., n - 1]"
