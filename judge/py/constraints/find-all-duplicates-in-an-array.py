"""Find All Duplicates in an Array: n integers in 1..n, each appearing once or twice."""

from collections import Counter


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= x <= n for x in nums), "1 <= nums[i] <= n"
    assert all(c <= 2 for c in Counter(nums).values()), "each element in nums appears once or twice"
