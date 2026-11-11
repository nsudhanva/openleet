"""Paint House IV at n = 2 * 10^4 houses (10^4 mirrored pairs), so trying colorings pair by pair
without memoization explodes where the six-state DP does ~3 * 10^5 transitions."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"n": N, "cost": [[rng.randint(0, 10**5) for _ in range(3)] for _ in range(N)]}
