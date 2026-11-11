"""Find the Median of the Uniqueness Array at n = 2 * 10^4, so counting the distinct values
of every subarray is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    top = rng.choice((10**5, 300))
    return {"nums": [rng.randint(1, top) for _ in range(N)]}
