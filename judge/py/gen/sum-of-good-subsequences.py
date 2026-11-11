"""Sum of Good Subsequences. Seed 0: n = 2 * 10^4 values in a narrow band, so extending every
earlier element that differs by one is ~2 * 10^8 pair checks. Seed 1: n = 3 * 10^4 distinct values
spread over [0, 10^5], so scanning every distinct value seen so far for each element is
~4.5 * 10^8 checks."""

from _shapes import pick_shape

SEEDS = 2
N = 2 * 10**4
N_WIDE = 3 * 10**4
TOP = 10**5


def generate(rng):
    if pick_shape(rng) == 2:
        return {"nums": rng.sample(range(TOP + 1), N_WIDE)}
    lo = rng.randint(0, TOP - 20)
    width = rng.randint(3, 20)
    return {"nums": [rng.randint(lo, lo + width) for _ in range(N)]}
