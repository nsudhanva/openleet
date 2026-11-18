"""Form Array by Concatenating Subarrays of Another Array: groups of integers and an array nums."""


def check(groups: list[list[int]], nums: list[int]) -> None:
    assert 1 <= len(groups) <= 10**3, "1 <= n <= 10^3"
    assert all(len(g) >= 1 for g in groups), "1 <= groups[i].length"
    assert sum(len(g) for g in groups) <= 10**3, "sum(groups[i].length) <= 10^3"
    assert 1 <= len(nums) <= 10**3, "1 <= nums.length <= 10^3"
    lim = 10**7
    assert all(-lim <= v <= lim for g in groups for v in g), "-10^7 <= groups[i][j] <= 10^7"
    assert all(-lim <= v <= lim for v in nums), "-10^7 <= nums[k] <= 10^7"
