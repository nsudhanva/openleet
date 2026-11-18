"""Maximum Product of First and Last Elements of a Subsequence: integers and a length m."""


def check(nums: list[int], m: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
    assert 1 <= m <= len(nums), "1 <= m <= nums.length"
