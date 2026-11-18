"""Missing Number: n distinct integers from 0..n."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert all(0 <= v <= n for v in nums), "0 <= nums[i] <= n"
    assert len(set(nums)) == n, "all the numbers of nums are unique"
