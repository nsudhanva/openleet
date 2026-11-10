"""Partition Equal Subset Sum at n = 200, values up to 100: a random even total, or all-even
values whose half-sum is odd so no split exists and the full O(n * sum) DP runs."""

SEEDS = 2
N = 200


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, 100) for _ in range(N)]
        if sum(nums) % 2:
            nums[0] = nums[0] + 1 if nums[0] < 100 else nums[0] - 1
    else:
        nums = [rng.randint(1, 50) * 2 for _ in range(N)]
        if sum(nums) % 4 == 0:
            nums[0] = nums[0] + 2 if nums[0] <= 98 else nums[0] - 2
    rng.shuffle(nums)
    return {"nums": nums}
