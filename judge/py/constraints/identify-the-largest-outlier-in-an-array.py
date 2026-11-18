"""Identify the Largest Outlier in an Array: n-2 special numbers, their sum and an outlier."""

from collections import Counter


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= nums.length <= 10^5"
    assert all(-1000 <= x <= 1000 for x in nums), "-1000 <= nums[i] <= 1000"
    total = sum(nums)
    counts = Counter(nums)
    ok = False
    for o in counts:
        rest = total - o
        if rest % 2:
            continue
        s = rest // 2
        if counts.get(s, 0) - (s == o) >= 1:
            ok = True
            break
    assert ok, "at least one potential outlier exists in nums"
