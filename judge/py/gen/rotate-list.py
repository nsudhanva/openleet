"""Rotate List at 500 nodes with k up to 2 * 10^9, so stepping k times is too slow."""

SEEDS = 3


def generate(rng):
    n = rng.choice([500, 499, 1])
    head = [rng.randint(-100, 100) for _ in range(n)]
    k = rng.choice([2 * 10**9, rng.randint(0, 2 * 10**9), 2 * 10**9 - 2 * 10**9 % n])
    return {"head": head, "k": k}
