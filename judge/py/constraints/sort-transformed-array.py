"""Sort Transformed Array: a sorted list and quadratic coefficients."""


def check(nums: list[int], a: int, b: int, c: int) -> None:
    assert 1 <= len(nums) <= 200, "1 <= nums.length <= 200"
    assert all(isinstance(v, int) and -100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
    assert all(isinstance(v, int) and -100 <= v <= 100 for v in (a, b, c)), "-100 <= a, b, c <= 100"
    assert all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)), (
        "nums is sorted in ascending order"
    )
