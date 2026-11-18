"""Maximum Score of a Good Subarray: an integer array and an index k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 2 * 10**4 for v in nums), "1 <= nums[i] <= 2 * 10^4"
    assert 0 <= k < len(nums), "0 <= k < nums.length"
