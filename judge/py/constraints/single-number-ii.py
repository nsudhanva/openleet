"""Single Number II: integers where one appears once and the rest three times."""

from collections import Counter


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 3 * 10**4, "1 <= nums.length <= 3 * 10^4"
    assert all(-(2**31) <= v <= 2**31 - 1 for v in nums), "-2^31 <= nums[i] <= 2^31 - 1"
    counts = Counter(nums)
    assert sum(c == 1 for c in counts.values()) == 1, "exactly one element appears once"
    assert all(c in (1, 3) for c in counts.values()), "every other element appears 3 times"
