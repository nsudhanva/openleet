"""Maximum Average Subarray II at n = 10^4 (the maximum) with k either at most 5 or close to n/3,
so checking every subarray of length at least k is ~5 * 10^7 steps and checking only the lengths
from k to 2k is ~1.7 * 10^7."""

from _shapes import pick_shape

SEEDS = 2
N = 10**4
LIMIT = 10**4


def generate(rng):
    k = rng.randint(1, 5) if pick_shape(rng) == 0 else rng.randint(N // 3 - N // 100, N // 3)
    return {"nums": [rng.randint(-LIMIT, LIMIT) for _ in range(N)], "k": k}
