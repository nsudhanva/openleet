"""Maximum Product After K Increments: non-negative integers and an increment count."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
    assert all(0 <= v <= 10**6 for v in nums), "0 <= nums[i] <= 10^6"
