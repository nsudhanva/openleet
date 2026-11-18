"""Set Mismatch: 1..n with one number duplicated over another."""

from collections import Counter


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 2 <= n <= 10**4, "2 <= nums.length <= 10^4"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
    assert all(v <= n for v in nums), "values come from 1..n"
    counts = Counter(nums)
    assert sorted(counts.values()).count(2) == 1 and max(counts.values()) == 2, (
        "exactly one number occurs twice"
    )
    assert len(counts) == n - 1, "exactly one number is missing"
