"""Minimum Cost to Connect Sticks at the maximum n = 10^4, so taking the two shortest sticks by
scanning each time is quadratic."""

SEEDS = 2
N = 10**4
LIMIT = 10**4


def generate(rng):
    return {"sticks": [rng.randint(1, LIMIT) for _ in range(N)]}
