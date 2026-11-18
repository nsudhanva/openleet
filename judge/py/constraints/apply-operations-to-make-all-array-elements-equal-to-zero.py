"""Apply Operations to Make All Array Elements Equal to Zero: non-negative integers and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= k <= len(nums) <= 10**5, "1 <= k <= nums.length <= 10^5"
    assert all(0 <= v <= 10**6 for v in nums), "0 <= nums[i] <= 10^6"
