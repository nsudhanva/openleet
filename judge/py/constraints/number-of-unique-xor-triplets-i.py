"""Number of Unique XOR Triplets I: a permutation of 1..n."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n == nums.length <= 10^5"
    assert sorted(nums) == list(range(1, n + 1)), "nums is a permutation of 1 to n"
