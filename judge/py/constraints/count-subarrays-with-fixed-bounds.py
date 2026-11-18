"""Count Subarrays With Fixed Bounds: an integer array and two bounds."""


def check(nums: list[int], minK: int, maxK: int) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
    assert 1 <= minK <= 10**6, "1 <= minK <= 10^6"
    assert 1 <= maxK <= 10**6, "1 <= maxK <= 10^6"
