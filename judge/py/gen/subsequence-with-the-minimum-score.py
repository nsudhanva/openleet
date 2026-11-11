"""Subsequence With the Minimum Score at |s| = |t| = 2 * 10^4 over 'ab': t is independent of s,
or a copy of s with letters s lacks scattered over 80-90% of its length, so the removed block is
long and searching linearly for its right end from every left end is ~1.6 * 10^8 steps."""

from _shapes import random_string

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    # The first draw picks the shape, so seeds 0 and 1 take different branches.
    independent = rng.random() < 0.5
    s = random_string(rng, "ab", N)
    if independent:
        t = random_string(rng, "ab", N)
    else:
        t = list(s)
        for p in rng.sample(range(8 * N // 10, 9 * N // 10), 50):
            t[p] = "c"
        t = "".join(t)
    return {"s": s, "t": t}
