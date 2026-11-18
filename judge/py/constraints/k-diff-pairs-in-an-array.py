"""K-diff Pairs in an Array: an integer array and a difference k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(-(10**7) <= v <= 10**7 for v in nums), "-10^7 <= nums[i] <= 10^7"
    assert 0 <= k <= 10**7, "0 <= k <= 10^7"
