"""Minimum Difference in Sums After Removal of Elements: an array of length 3 * n."""


def check(nums: list[int]) -> None:
    assert len(nums) % 3 == 0, "nums.length == 3 * n"
    n = len(nums) // 3
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= x <= 10**5 for x in nums), "1 <= nums[i] <= 10^5"
