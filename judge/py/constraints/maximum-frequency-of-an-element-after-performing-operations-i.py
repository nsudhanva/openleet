"""Maximum Frequency of an Element After Performing Operations I: an array, k and numOperations."""


def check(nums: list[int], k: int, numOperations: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert 0 <= k <= 10**5, "0 <= k <= 10^5"
    assert 0 <= numOperations <= len(nums), "0 <= numOperations <= nums.length"
