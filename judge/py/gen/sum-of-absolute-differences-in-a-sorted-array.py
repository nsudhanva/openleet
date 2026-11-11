"""Sum of Absolute Differences in a Sorted Array at n = 3 * 10^4 sorted values with many repeats,
so summing |x - y| over every pair is ~9 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    hi = rng.choice((10**4, 500))
    return {"nums": sorted(rng.randint(1, hi) for _ in range(N))}
