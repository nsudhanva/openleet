"""Contains Duplicate II at n = 10^5 with k up to 10^5: distinct values with at most one
equal pair near the end, so a window scan of size k does the most work."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = rng.sample(range(-(10**9), 10**9 + 1), N)
    k = rng.randint(N // 2, N)
    shape = rng.randrange(3)
    if shape == 1:
        nums[-1] = nums[-1 - k] if k < N else nums[0]
    elif shape == 2:
        gap = min(k + 1, N - 1)
        nums[-1] = nums[-1 - gap]
    return {"nums": nums, "k": k}
