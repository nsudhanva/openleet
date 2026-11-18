"""Max Consecutive Ones III: a binary array and a flip budget."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(v in (0, 1) for v in nums), "nums[i] is either 0 or 1"
    assert 0 <= k <= len(nums), "0 <= k <= nums.length"
