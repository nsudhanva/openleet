"""Open the Lock with 500 distinct deadends and a far target, so BFS explores most of the
10^4 states."""

from _shapes import random_string

SEEDS = 2
DEADENDS = 500


def generate(rng):
    target = random_string(rng, "456", 4)
    pool = [f"{i:04d}" for i in range(1, 10**4) if f"{i:04d}" != target]
    deadends = rng.sample(pool, DEADENDS)
    return {"deadends": deadends, "target": target}
