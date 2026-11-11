"""nums of 2 * 10^4 values, so even an O(n^2) pass over all pairs costs ~4 * 10^8 steps (the
direct loop over triplets, ~8 * 10^12)."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"nums": [rng.randint(1, 10**9) for _ in range(N)]}
