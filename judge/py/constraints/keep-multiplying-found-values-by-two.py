"""Keep Multiplying Found Values by Two: an integer array and a starting value."""


def check(nums: list[int], original: int) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
    assert 1 <= original <= 1000, "1 <= original <= 1000"
