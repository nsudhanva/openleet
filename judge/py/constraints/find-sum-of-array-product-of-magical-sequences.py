"""Find Sum of Array Product of Magical Sequences: m, k and values nums."""


def check(m: int, k: int, nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= k <= m <= 30, "1 <= k <= m <= 30"
    assert 1 <= len(nums) <= 50, "1 <= nums.length <= 50"
    assert all(1 <= v <= 10**8 for v in nums), "1 <= nums[i] <= 10^8"
