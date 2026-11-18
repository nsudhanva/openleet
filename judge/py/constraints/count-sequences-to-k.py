"""Count Sequences to K: digits 1..6 in a short array and a target k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 19, "1 <= nums.length <= 19"
    assert all(1 <= v <= 6 for v in nums), "1 <= nums[i] <= 6"
    assert 1 <= k <= 10**15, "1 <= k <= 10^15"
