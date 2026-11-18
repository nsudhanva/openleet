"""Create Target Array in the Given Order: values and insertion indices of equal length."""


def check(nums: list[int], index: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert 1 <= len(index) <= 100, "1 <= index.length <= 100"
    assert len(nums) == len(index), "nums.length == index.length"
    assert all(0 <= v <= 100 for v in nums), "0 <= nums[i] <= 100"
    assert all(0 <= v <= i for i, v in enumerate(index)), "0 <= index[i] <= i"
