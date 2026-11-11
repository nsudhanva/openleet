"""Triples with Bitwise AND Zero at the maximum n = 1000 distinct values, all the subsets of 10 or
11 random bits, so the pairwise ANDs stay in that family of at most 2048 masks (counting pair ANDs
is ~3 * 10^6 steps) while the triple loop, even over distinct values, is 10^9."""

SEEDS = 2
N = 1000


def generate(rng):
    bits = rng.sample(range(16), rng.choice([10, 11]))
    family = []
    for sub in range(1 << len(bits)):
        family.append(sum(1 << b for i, b in enumerate(bits) if sub >> i & 1))
    return {"nums": rng.sample(family, min(N, len(family)))}
