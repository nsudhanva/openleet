"""Find Score of an Array After Marking All Elements at n = 2 * 10^4 random values, so finding
each next smallest unmarked value by a scan is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    top = rng.choice((10**6, 100))
    return {"nums": [rng.randint(1, top) for _ in range(N)]}
