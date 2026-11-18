"""Make Lexicographically Smallest Array by Swapping Elements: an array and a swap limit."""


def check(nums: list[int], limit: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= limit <= 10**9, "1 <= limit <= 10^9"
