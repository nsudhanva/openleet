"""Find the Maximum Length of Valid Subsequence II: an array and a modulus k."""


def check(nums: list[int], k: int) -> None:
    assert 2 <= len(nums) <= 10**3, "2 <= nums.length <= 10^3"
    assert all(1 <= v <= 10**7 for v in nums), "1 <= nums[i] <= 10^7"
    assert 1 <= k <= 10**3, "1 <= k <= 10^3"
