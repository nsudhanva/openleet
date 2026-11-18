"""Count of Range Sum: 32-bit integers with bounds lower and upper."""


def check(nums: list[int], lower: int, upper: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(2**31) <= v <= 2**31 - 1 for v in nums), "-2^31 <= nums[i] <= 2^31 - 1"
    assert -(10**5) <= lower <= upper <= 10**5, "-10^5 <= lower <= upper <= 10^5"
