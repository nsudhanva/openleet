"""Maximum XOR After Operations: an array of non-negative ints."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**8 for v in nums), "0 <= nums[i] <= 10^8"
