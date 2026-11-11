"""Maximize Greatness of an Array at n = 2 * 10^4 values with repeats, so matching each value to
the smallest unused larger one by scanning is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**9


def generate(rng):
    pool = [rng.randint(0, TOP) for _ in range(N // 4)]
    return {"nums": [rng.choice(pool) for _ in range(N)]}
