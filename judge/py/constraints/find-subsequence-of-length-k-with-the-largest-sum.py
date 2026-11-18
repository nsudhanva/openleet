"""Find Subsequence of Length K With the Largest Sum: an integer array and a length k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
