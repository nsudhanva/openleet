"""Count Subarrays Where Max Element Appears at Least K Times: an integer array and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
