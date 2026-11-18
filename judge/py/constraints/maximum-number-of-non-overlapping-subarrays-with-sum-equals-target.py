"""Maximum Number of Non-Overlapping Subarrays With Sum Equals Target: an integer array and a
target."""


def check(nums: list[int], target: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
    assert 0 <= target <= 10**6, "0 <= target <= 10^6"
