"""Make the XOR of All Segments Equal to Zero: an array of 10-bit values and a segment size k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= k <= len(nums) <= 2000, "1 <= k <= nums.length <= 2000"
    assert all(0 <= v < 2**10 for v in nums), "0 <= nums[i] < 2^10"
