"""Most Frequent Number Following Key In an Array: an integer array and a key present in it."""

import itertools
from collections import Counter


def check(nums: list[int], key: int) -> None:
    assert 2 <= len(nums) <= 1000, "2 <= nums.length <= 1000"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
    assert key in nums, "key is present in nums"
    counts = Counter(b for a, b in itertools.pairwise(nums) if a == key)
    top = counts.most_common(2)
    assert top, "key is followed by some number"
    assert len(top) == 1 or top[0][1] > top[1][1], "the answer is unique"
