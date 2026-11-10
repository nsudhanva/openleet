"""Minimum Time Difference with 2 * 10^4 time points: all distinct-ish random times (so
duplicates appear) or a sparse set of distinct times; pairwise comparison is 2 * 10^8."""

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        minutes = [rng.randrange(1440) for _ in range(N)]
    else:
        minutes = rng.sample(range(1440), rng.randint(2, 1440))
    return {"timePoints": [f"{m // 60:02d}:{m % 60:02d}" for m in minutes]}
