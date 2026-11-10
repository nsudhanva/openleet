"""Wiggle Subsequence at the maximum n = 1000 with long flat runs and monotone stretches, so
equal neighbours and plateaus must be handled."""

from _shapes import pick_shape

SEEDS = 3
N = 1000


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        nums = [rng.randint(0, 1000) for _ in range(N)]
    elif shape == 1:
        nums = []
        while len(nums) < N:
            nums.extend([rng.randint(0, 1000)] * rng.randint(1, 20))
        nums = nums[:N]
    else:
        nums = sorted(rng.randint(0, 1000) for _ in range(N))
    return {"nums": nums}
