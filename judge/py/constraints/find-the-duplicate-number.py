"""Find the Duplicate Number: n + 1 integers in [1, n] with exactly one repeated value."""

from collections import Counter


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    n = len(nums) - 1
    assert 1 <= n <= 10**5, "1 <= n <= 10^5, nums.length == n + 1"
    assert all(1 <= v <= n for v in nums), "1 <= nums[i] <= n"
    repeated = [v for v, c in Counter(nums).items() if c >= 2]
    assert len(repeated) == 1, "exactly one integer appears two or more times, the rest once"
