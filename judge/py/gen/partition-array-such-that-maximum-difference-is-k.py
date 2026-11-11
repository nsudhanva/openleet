"""Partition Array Such That Maximum Difference Is K at the maximum 10^5 values with k <= 2,
so ~2 * 10^4 groups are needed and peeling one group per pass over the rest does ~10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    return {"nums": [rng.randint(0, 10**5) for _ in range(N)], "k": rng.randint(0, 2)}
