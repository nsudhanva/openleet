"""Subarray Sum Equals K at n = 2 * 10^4: all zeros with k = 0 (2 * 10^8 matching subarrays)
or small values with a common target, punishing the quadratic scan."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        return {"nums": [0] * N, "k": 0}
    if shape == 1:
        nums = [rng.randint(-3, 3) for _ in range(N)]
        return {"nums": nums, "k": rng.randint(-5, 5)}
    nums = [rng.randint(-1000, 1000) for _ in range(N)]
    return {"nums": nums, "k": rng.randint(-5000, 5000)}
