"""Recover the Original Array: 2n numbers made of arr - k and arr + k."""

from collections import Counter


def _splits(nums: list[int], k: int) -> bool:
    counts = Counter(nums)
    for v in sorted(counts):
        c = counts[v]
        if c == 0:
            continue
        if counts.get(v + 2 * k, 0) < c:
            return False
        counts[v + 2 * k] -= c
    return True


def check(nums: list[int]) -> None:
    assert len(nums) % 2 == 0, "2 * n == nums.length"
    assert 1 <= len(nums) // 2 <= 1000, "1 <= n <= 1000"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    lo = min(nums)
    ks = {(v - lo) // 2 for v in nums if v > lo and (v - lo) % 2 == 0}
    assert any(_splits(nums, k) for k in ks), "at least one valid array arr exists"
