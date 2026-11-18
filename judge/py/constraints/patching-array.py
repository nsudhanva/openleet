"""Patching Array: a sorted array of positive integers and a target n."""


def check(nums: list[int], n: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(isinstance(v, int) and 1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
    assert all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)), (
        "nums is sorted in ascending order"
    )
    assert isinstance(n, int) and 1 <= n <= 2**31 - 1, "1 <= n <= 2^31 - 1"
