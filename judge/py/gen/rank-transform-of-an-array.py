"""Rank Transform at n = 10^5: full-range values, or few distinct values with heavy
duplication."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        arr = [rng.randint(-(10**9), 10**9) for _ in range(N)]
    else:
        pool = [rng.randint(-(10**9), 10**9) for _ in range(100)]
        arr = [rng.choice(pool) for _ in range(N)]
    return {"arr": arr}
