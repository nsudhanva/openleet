"""Sum of Distances at n = 3 * 10^4 with only two or three distinct values, so summing the
distance to every equal element is ~3 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    values = rng.sample(range(10**9 + 1), rng.randint(2, 3))
    return {"nums": [rng.choice(values) for _ in range(N)]}
