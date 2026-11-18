"""Minimum Number of Removals to Make Mountain Array: an integer array that contains a
mountain subsequence."""

from bisect import bisect_left


def _lis(a: list[int]) -> list[int]:
    tails: list[int] = []
    out = []
    for v in a:
        i = bisect_left(tails, v)
        if i == len(tails):
            tails.append(v)
        else:
            tails[i] = v
        out.append(i + 1)
    return out


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    n = len(nums)
    assert 3 <= n <= 1000, "3 <= nums.length <= 1000"
    assert all(isinstance(v, int) and 1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    left = _lis(nums)
    right = _lis(nums[::-1])[::-1]
    assert any(left[i] > 1 and right[i] > 1 for i in range(1, n - 1)), (
        "you can make a mountain array out of nums"
    )
