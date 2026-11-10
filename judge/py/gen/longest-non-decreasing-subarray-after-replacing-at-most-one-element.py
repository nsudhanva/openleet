"""Longest Non-Decreasing Subarray After One Replacement at n = 10^5: long sorted runs split by
single dips, or random values."""

SEEDS = 3
N = 10**5
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.6:
        nums = sorted(rng.randint(-LIMIT, LIMIT) for _ in range(N))
        for _ in range(rng.randint(1, 50)):
            i = rng.randrange(N)
            nums[i] = rng.randint(-LIMIT, LIMIT)
    else:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    return {"nums": nums}
