"""Ways to Split Array Into Three Subarrays: a list of non-negative integers."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**4 for v in nums), "0 <= nums[i] <= 10^4"
