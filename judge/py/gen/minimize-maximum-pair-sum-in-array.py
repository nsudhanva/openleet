"""Minimize Maximum Pair Sum in Array at n = 5 * 10^4, so pairing by repeatedly scanning for the
smallest and largest remaining values is quadratic."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 10**5


def generate(rng):
    return {"nums": [rng.randint(1, LIMIT) for _ in range(N)]}
