"""Magnetic Force at n = 10^5 distinct positions up to 10^9, with m from 2 to n, so trying
every distance is far too slow."""

SEEDS = 3
N = 10**5


def generate(rng):
    position = rng.sample(range(1, 10**9 + 1), N)
    m = rng.choice([2, N, rng.randint(2, N), rng.randint(2, 100)])
    return {"position": position, "m": m}
