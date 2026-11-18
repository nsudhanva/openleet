"""Find if Array Can Be Sorted: a short list of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= v <= 2**8 for v in nums), "1 <= nums[i] <= 2^8"
