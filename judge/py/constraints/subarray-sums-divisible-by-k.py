"""Subarray Sums Divisible by K: integers and a divisor k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 3 * 10**4, "1 <= nums.length <= 3 * 10^4"
    assert all(isinstance(v, int) and -(10**4) <= v <= 10**4 for v in nums), (
        "-10^4 <= nums[i] <= 10^4"
    )
    assert isinstance(k, int) and 2 <= k <= 10**4, "2 <= k <= 10^4"
