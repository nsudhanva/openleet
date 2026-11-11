"""Maximize Happiness of Selected Children at n = 2 * 10^4 with k in [n / 2, n], so picking the
happiest child and lowering everyone else turn by turn is >= 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**8


def generate(rng):
    happiness = [rng.randint(1, TOP) if rng.random() < 0.7 else rng.randint(1, N) for _ in range(N)]
    return {"happiness": happiness, "k": rng.randint(N // 2, N)}
