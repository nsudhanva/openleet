"""Maximum Square Area by Removing Fences at the maximum 600 fences each way on a ~10^9 field,
so comparing every pair of gaps costs ~3 * 10^10 steps."""

SEEDS = 2
F = 600
SIDE = 10**9


def generate(rng):
    m, n = rng.randint(SIDE // 2, SIDE), rng.randint(SIDE // 2, SIDE)
    return {
        "m": m,
        "n": n,
        "hFences": rng.sample(range(2, m), F),
        "vFences": rng.sample(range(2, n), F),
    }
