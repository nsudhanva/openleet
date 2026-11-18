"""Maximum Score from Performing Multiplication Operations: two integer arrays, nums at
least as long as multipliers."""


def check(nums: list[int], multipliers: list[int]) -> None:
    n, m = len(nums), len(multipliers)
    assert 1 <= m <= 300, "1 <= m <= 300"
    assert m <= n <= 10**5, "m <= n <= 10^5"
    assert all(-1000 <= v <= 1000 for v in nums), "-1000 <= nums[i] <= 1000"
    assert all(-1000 <= v <= 1000 for v in multipliers), "-1000 <= multipliers[i] <= 1000"
