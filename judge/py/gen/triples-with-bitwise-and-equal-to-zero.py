"""Triples with Bitwise AND Zero at n = 1000, where the O(n^3) triple loop is 10^9 steps:
random 16-bit values or sparse masks with many zero ANDs."""

SEEDS = 2
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randrange(2**16) for _ in range(N)]
    else:
        nums = [1 << rng.randrange(16) | 1 << rng.randrange(16) for _ in range(N)]
    return {"nums": nums}
