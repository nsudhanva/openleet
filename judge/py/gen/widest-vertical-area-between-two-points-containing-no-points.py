"""Widest Vertical Area at 2 * 10^4 points with random coordinates, so finding each point's
next x to the right by scanning is ~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**9


def generate(rng):
    return {"points": [[rng.randint(0, TOP), rng.randint(0, TOP)] for _ in range(N)]}
