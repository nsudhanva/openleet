"""Tallest Billboard at the maximum 20 rods with the sum near 5000, so 3^20 brute force is
hopeless and only the difference DP is fast."""

from _shapes import pick_shape

SEEDS = 3
N = 20
SUM = 5000


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        rods = [rng.randint(1, 500) for _ in range(N)]
    elif shape == 1:
        rods = [rng.choice([1, 2, 3, 997, 1000]) for _ in range(N)]
    else:
        rods = [rng.randint(1, 1000) for _ in range(N)]
    # Scale down until the sum fits.
    while sum(rods) > SUM:
        i = max(range(N), key=lambda j: rods[j])
        rods[i] = max(1, rods[i] - (sum(rods) - SUM))
    return {"rods": rods}
