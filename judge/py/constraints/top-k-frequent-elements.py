"""Top K Frequent Elements: an integer array and k, with a unique answer."""

from collections import Counter


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**4) <= x <= 10**4 for x in nums), "-10^4 <= nums[i] <= 10^4"
    counts = sorted(Counter(nums).values(), reverse=True)
    assert 1 <= k <= len(counts), "k is in the range [1, the number of unique elements]"
    assert k == len(counts) or counts[k - 1] > counts[k], "the answer is unique"
