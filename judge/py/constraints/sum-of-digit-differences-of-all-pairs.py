"""Sum of Digit Differences of All Pairs: positive integers of equal digit count."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(1 <= x < 10**9 for x in nums), "1 <= nums[i] < 10^9"
    assert len({len(str(x)) for x in nums}) == 1, (
        "all integers in nums have the same number of digits"
    )
