"""Minimum Operations to Convert All Elements to Zero at n = 2 * 10^4 on a nearly increasing array,
so zeroing a segment's minimum and recursing on the pieces peels one element per pass and is
quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    nums = sorted(rng.choices(range(1, LIMIT + 1), k=N))
    for i in range(N - 1):
        if rng.random() < 0.3:
            nums[i], nums[i + 1] = nums[i + 1], nums[i]
    return {"nums": nums}
