"""Two Sum: an integer array and a target with exactly one valid pair."""

from collections import Counter


def check(nums: list[int], target: int) -> None:
    assert 2 <= len(nums) <= 10**4, "2 <= nums.length <= 10^4"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert -(10**9) <= target <= 10**9, "-10^9 <= target <= 10^9"
    c = Counter(nums)
    pairs = 0
    for v, k in c.items():
        w = target - v
        if v < w:
            pairs += k * c.get(w, 0)
        elif v == w:
            pairs += k * (k - 1) // 2
    assert pairs == 1, "only one valid answer exists"
