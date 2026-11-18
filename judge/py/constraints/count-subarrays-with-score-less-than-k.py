"""Count Subarrays With Score Less Than K: positive integers and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert 1 <= k <= 10**15, "1 <= k <= 10^15"
