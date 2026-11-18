"""Number of Ways to Reorder Array to Get Same BST: a permutation of 1..n."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= n for v in nums), "1 <= nums[i] <= nums.length"
    assert len(set(nums)) == n, "all integers in nums are distinct"
