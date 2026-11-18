"""Maximum Sum of Distinct Subarrays With Length K: an array of positive ints and a length k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= k <= len(nums) <= 10**5, "1 <= k <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
