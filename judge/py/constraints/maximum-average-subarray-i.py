"""Maximum Average Subarray I: an integer array and a window length k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= k <= n <= 10**5, "1 <= k <= n <= 10^5"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
