"""3Sum Smaller: a list of small integers and a target."""

from collections import Counter
from math import comb


def check(nums: list[int], target: int) -> None:
    n = len(nums)
    assert 0 <= n <= 3500, "0 <= n <= 3500"
    assert all(-100 <= x <= 100 for x in nums), "-100 <= nums[i] <= 100"
    assert -100 <= target <= 100, "-100 <= target <= 100"
    counts = sorted(Counter(nums).items())
    total = 0
    for i, (a, ca) in enumerate(counts):
        for j in range(i, len(counts)):
            b, cb = counts[j]
            for k in range(j, len(counts)):
                c, cc = counts[k]
                if a + b + c >= target:
                    break
                if i == j == k:
                    total += comb(ca, 3)
                elif i == j:
                    total += comb(ca, 2) * cc
                elif j == k:
                    total += ca * comb(cb, 2)
                else:
                    total += ca * cb * cc
    assert total <= 10**9, "the answer is less than or equal to 10^9"
