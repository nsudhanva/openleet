"""Find Missing Elements: unique integers drawn from a range with gaps."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert len(set(nums)) == len(nums), "nums consists of unique integers"
