"""Split Array Largest Sum: a non-negative array and a piece count k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(0 <= v <= 10**6 for v in nums), "0 <= nums[i] <= 10^6"
    assert 1 <= k <= min(50, len(nums)), "1 <= k <= min(50, nums.length)"
