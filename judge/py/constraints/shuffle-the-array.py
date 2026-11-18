"""Shuffle the Array: 2n integers and n."""


def check(nums: list[int], n: int) -> None:
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert len(nums) == 2 * n, "nums.length == 2n"
    assert all(1 <= v <= 10**3 for v in nums), "1 <= nums[i] <= 10^3"
