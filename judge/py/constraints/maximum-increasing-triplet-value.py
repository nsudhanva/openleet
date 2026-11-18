"""Maximum Increasing Triplet Value: an integer array with at least one increasing triplet."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 3 <= n <= 10**5, "3 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    suffix_max = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_max[i] = max(suffix_max[i + 1], nums[i])
    low = nums[0]
    for j in range(1, n - 1):
        if low < nums[j] < suffix_max[j + 1]:
            return
        low = min(low, nums[j])
    raise AssertionError("at least one triplet i < j < k with nums[i] < nums[j] < nums[k] exists")
