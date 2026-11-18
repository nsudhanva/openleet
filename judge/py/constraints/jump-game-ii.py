"""Jump Game II: an array of maximum jump lengths, last index reachable."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    n = len(nums)
    assert 1 <= n <= 10**4, "1 <= nums.length <= 10^4"
    assert all(0 <= v <= 1000 for v in nums), "0 <= nums[i] <= 1000"
    far = 0
    for i, v in enumerate(nums):
        assert i <= far, "it's guaranteed that you can reach nums[n - 1]"
        far = max(far, i + v)
