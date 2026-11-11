"""Reach End of Array With Max Score at n = 10^4, so the quadratic jump DP does ~5 * 10^7
transitions."""

SEEDS = 2
N = 10**4


def generate(rng):
    nums = [rng.randint(1, 10**5) for _ in range(N)]
    if rng.random() < 0.5:
        nums.sort()
    return {"nums": nums}
