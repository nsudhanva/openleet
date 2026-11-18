"""Path Sum IV: a binary tree of depth below 5 encoded as three-digit integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 15, "1 <= nums.length <= 15"
    assert all(isinstance(v, int) and 110 <= v <= 489 for v in nums), "110 <= nums[i] <= 489"
    assert all(nums[i] < nums[i + 1] for i in range(len(nums) - 1)), (
        "nums is sorted in ascending order"
    )
    present = {v // 10 for v in nums}
    for v in nums:
        d, p = v // 100, v // 10 % 10
        assert 1 <= d <= 4 and 1 <= p <= 2 ** (d - 1), (
            "depth less than 5, position within the level"
        )
        assert d == 1 or (d - 1) * 10 + (p + 1) // 2 in present, (
            "nums represents a valid binary tree"
        )
    assert 11 in present, "nums represents a valid binary tree"
