"""Maximum Score After Binary Swaps: integers and a binary string of the same length."""


def check(nums: list[int], s: str) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= n <= 10^5"
    assert len(s) == len(nums), "n == nums.length == s.length"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert all(c in "01" for c in s), "s[i] is either '0' or '1'"
