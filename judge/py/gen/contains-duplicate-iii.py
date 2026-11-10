"""Contains Duplicate III at n = 10^5 with a huge indexDiff: values spaced more than valueDiff
apart (answer false after a full scan), optionally with one close pair planted at the end."""

SEEDS = 3
N = 10**5


def generate(rng):
    value_diff = rng.randint(0, 1000)
    step = value_diff + 1 + rng.randint(0, 10)
    base = -(10**9)
    nums = [base + i * step for i in range(N)]
    if rng.random() < 0.5:
        rng.shuffle(nums)
    if rng.random() < 0.5:
        nums[-1] = nums[0] + rng.randint(-value_diff, value_diff)
        nums[-1] = max(-(10**9), min(10**9, nums[-1]))
    index_diff = rng.randint(N - 10, N)
    return {"nums": nums, "indexDiff": index_diff, "valueDiff": value_diff}
