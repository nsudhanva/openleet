"""Find the K-or of an Array: an integer array and a bit-count threshold k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 50, "1 <= nums.length <= 50"
    assert all(0 <= v < 2**31 for v in nums), "0 <= nums[i] < 2^31"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
