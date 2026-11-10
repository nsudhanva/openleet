"""Minimum Time to Repair Cars with 10^5 mechanics and up to 10^6 cars; one seed with a single
slow mechanic so the answer is 10^14."""

SEEDS = 3
N = 10**5


def generate(rng):
    n = rng.choice((N, 1, rng.randint(1, N)))
    ranks = [rng.randint(1, 100) for _ in range(n)]
    return {"ranks": ranks, "cars": rng.choice((10**6, rng.randint(1, 10**6)))}
