"""K Divisible Elements Subarrays: an integer array, k and a divisor p."""


def check(nums: list[int], k: int, p: int) -> None:
    assert 1 <= len(nums) <= 200, "1 <= nums.length <= 200"
    assert all(1 <= v <= 200 for v in nums), "1 <= nums[i] <= 200"
    assert 1 <= p <= 200, "1 <= p <= 200"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
