"""Subarray Product Less Than K at n = 3 * 10^4: all ones with a huge k (every one of the
~4.5 * 10^8 subarrays counts), or small values so windows grow long."""

from _shapes import pick_shape

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        return {"nums": [1] * N, "k": 10**6}
    if shape == 1:
        nums = [rng.choice([1, 1, 1, 2]) for _ in range(N)]
        return {"nums": nums, "k": rng.randint(10**5, 10**6)}
    nums = [rng.randint(1, 1000) for _ in range(N)]
    return {"nums": nums, "k": rng.randint(0, 10**6)}
