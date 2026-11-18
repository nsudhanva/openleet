"""Jump Game VIII: arrays nums and costs of equal length."""


def check(nums: list[int], costs: list[int]) -> None:
    assert isinstance(nums, list) and isinstance(costs, list), "nums and costs are lists"
    assert len(nums) == len(costs), "n == nums.length == costs.length"
    assert 1 <= len(nums) <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
    assert all(0 <= v <= 10**5 for v in costs), "0 <= costs[i] <= 10^5"
