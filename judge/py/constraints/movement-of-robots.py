"""Movement of Robots: unique robot positions, directions 'L'/'R' and a time d."""


def check(nums: list[int], s: str, d: int) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(-2 * 10**9 <= v <= 2 * 10**9 for v in nums), "-2 * 10^9 <= nums[i] <= 2 * 10^9"
    assert 0 <= d <= 10**9, "0 <= d <= 10^9"
    assert len(nums) == len(s), "nums.length == s.length"
    assert set(s) <= set("LR"), "s consists of 'L' and 'R' only"
    assert len(set(nums)) == len(nums), "nums[i] will be unique"
