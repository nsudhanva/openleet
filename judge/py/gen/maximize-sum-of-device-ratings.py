"""Maximize Sum of Device Ratings at 10^4 devices of 3 units, so trying each device as the one that
receives every donated unit and re-adding the others is 10^8 steps."""

SEEDS = 2
M = 10**4
UNITS = 3
TOP = 10**5


def generate(rng):
    return {"units": [[rng.randint(1, TOP) for _ in range(UNITS)] for _ in range(M)]}
