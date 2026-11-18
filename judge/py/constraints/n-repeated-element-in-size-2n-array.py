"""N-Repeated Element in Size 2N Array: 2n integers, one value repeated n times, the rest unique."""

from collections import Counter


def check(nums: list[int]) -> None:
    assert len(nums) % 2 == 0, "nums.length == 2 * n"
    n = len(nums) // 2
    assert 2 <= n <= 5000, "2 <= n <= 5000"
    assert all(0 <= v <= 10**4 for v in nums), "0 <= nums[i] <= 10^4"
    counts = Counter(nums)
    assert len(counts) == n + 1, "nums contains n + 1 unique elements"
    assert sum(c == n for c in counts.values()) == 1, "one of them is repeated exactly n times"
