"""Count Subarrays With More Ones Than Zeros: a binary array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(v in (0, 1) for v in nums), "0 <= nums[i] <= 1"
