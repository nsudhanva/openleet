"""Partition Array to Minimize XOR at the maximum n = 250 with k between 20 and 40, so
enumerating the C(249, k - 1) ways to cut explodes and recomputing each segment's XOR does
~10^8 steps where the O(n^2 * k) DP with prefix XORs does ~2 * 10^6."""

SEEDS = 2
N = 250


def generate(rng):
    return {"nums": [rng.randint(1, 10**9) for _ in range(N)], "k": rng.randint(20, 40)}
