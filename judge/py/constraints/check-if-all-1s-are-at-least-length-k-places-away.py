"""Check If All 1's Are at Least Length K Places Away: a 0/1 array and k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert 0 <= k <= len(nums), "0 <= k <= nums.length"
    assert all(v in (0, 1) for v in nums), "nums[i] is 0 or 1"
