"""Maximum XOR of Two Numbers in an Array: an array of non-negative 31-bit ints."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2 * 10**5, "1 <= nums.length <= 2 * 10^5"
    assert all(0 <= v <= 2**31 - 1 for v in nums), "0 <= nums[i] <= 2^31 - 1"
