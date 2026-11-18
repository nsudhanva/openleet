"""Minimum Cost to Make Array Equal: values and per-value change costs."""


def check(nums: list[int], cost: list[int]) -> None:
    n = len(nums)
    assert n == len(cost), "n == nums.length == cost.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= x <= 10**6 for x in nums), "1 <= nums[i] <= 10^6"
    assert all(1 <= x <= 10**6 for x in cost), "1 <= cost[i] <= 10^6"
    # Weighted median gives the optimal target; the answer must not exceed 2^53 - 1.
    order = sorted(range(n), key=nums.__getitem__)
    half = (sum(cost) + 1) // 2
    acc = 0
    target = nums[order[0]]
    for i in order:
        acc += cost[i]
        if acc >= half:
            target = nums[i]
            break
    total = sum(abs(a - target) * c for a, c in zip(nums, cost, strict=True))
    assert total <= 2**53 - 1, "the output does not exceed 2^53 - 1"
