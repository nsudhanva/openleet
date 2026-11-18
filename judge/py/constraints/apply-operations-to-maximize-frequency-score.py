"""Apply Operations to Maximize Frequency Score: positive integers and an operation budget k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 0 <= k <= 10**14, "0 <= k <= 10^14"
