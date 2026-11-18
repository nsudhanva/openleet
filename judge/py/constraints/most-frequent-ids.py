"""Most Frequent IDs: parallel arrays of IDs and signed frequency changes."""

from collections import defaultdict


def check(nums: list[int], freq: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert len(nums) == len(freq), "nums.length == freq.length"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert all(-(10**5) <= f <= 10**5 for f in freq), "-10^5 <= freq[i] <= 10^5"
    assert all(f != 0 for f in freq), "freq[i] != 0"
    counts: dict[int, int] = defaultdict(int)
    for x, f in zip(nums, freq, strict=True):
        counts[x] += f
        assert counts[x] >= 0, "occurrences of an ID are never negative in any step"
