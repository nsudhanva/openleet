"""Minimize Max Distance to Gas Station with 2000 random stations and k = 10^6, so placing the
stations one at a time by scanning every gap is 2 * 10^9 steps."""

SEEDS = 2
N = 2000
K = 10**6
LIMIT = 10**8


def generate(rng):
    stations = sorted(rng.sample(range(LIMIT + 1), N))
    return {"stations": stations, "k": K}
