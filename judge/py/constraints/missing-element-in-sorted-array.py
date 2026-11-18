"""Missing Element in Sorted Array: a sorted array of unique integers and k."""

import itertools


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 5 * 10**4, "1 <= nums.length <= 5 * 10^4"
    assert all(1 <= v <= 10**7 for v in nums), "1 <= nums[i] <= 10^7"
    assert all(a < b for a, b in itertools.pairwise(nums)), (
        "nums is sorted in ascending order with unique elements"
    )
    assert 1 <= k <= 10**8, "1 <= k <= 10^8"
