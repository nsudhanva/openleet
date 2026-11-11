"""Count the Number of Incremovable Subarrays II at n = 2 * 10^4: two long increasing runs with
interleaved values, so tens of millions of removals are valid and checking every pair of ends
costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    vals = rng.sample(range(1, LIMIT + 1), N)
    cut = rng.randint(N // 3, 2 * N // 3)
    return {"nums": sorted(vals[:cut]) + sorted(vals[cut:])}
