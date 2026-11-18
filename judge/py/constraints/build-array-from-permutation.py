"""Build Array from Permutation: distinct values 0..n-1."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 1000, "1 <= nums.length <= 1000"
    assert all(0 <= v < n for v in nums), "0 <= nums[i] < nums.length"
    assert len(set(nums)) == n, "The elements in nums are distinct"
