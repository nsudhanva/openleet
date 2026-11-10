"""Shifting Letters at n = 10^5 with shifts up to 10^9 (prefix sums overflow 32 bits), so the
quadratic per-prefix approach does 5 * 10^9 work."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    all_max = rng.random() < 0.5
    n = 10**5
    s = random_string(rng, ascii_lowercase, n)
    shifts = [10**9] * n if all_max else [rng.randint(0, 10**9) for _ in range(n)]
    return {"s": s, "shifts": shifts}
