"""Sum of Good Subsequences at n = 2 * 10^4 values in a narrow band, so extending every earlier
element that differs by one is ~2 * 10^8 pair checks."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    lo = rng.randint(0, 10**5 - 20)
    width = rng.randint(3, 20)
    return {"nums": [rng.randint(lo, lo + width) for _ in range(N)]}
