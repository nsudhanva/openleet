"""Maximum Frequency of an Element After Performing Operations II: an array, k and numOperations."""


def check(nums: list[int], k: int, numOperations: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 0 <= k <= 10**9, "0 <= k <= 10^9"
    assert 0 <= numOperations <= len(nums), "0 <= numOperations <= nums.length"
