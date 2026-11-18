"""Combination Sum IV: distinct positive numbers and a target."""


def check(nums: list[int], target: int) -> None:
    assert 1 <= len(nums) <= 200, "1 <= nums.length <= 200"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
    assert len(set(nums)) == len(nums), "all the elements of nums are unique"
    assert 1 <= target <= 1000, "1 <= target <= 1000"
    ways = [1] + [0] * target
    for t in range(1, target + 1):
        ways[t] = sum(ways[t - v] for v in nums if v <= t)
    assert ways[target] < 2**31, "the answer fits in a 32-bit integer"
