"""Prison Cells After N Days with n near 10^9, so day-by-day simulation is far too slow and the
cycle must be found."""

SEEDS = 2
LOW, HIGH = 9 * 10**8, 10**9


def generate(rng):
    return {"cells": [rng.randint(0, 1) for _ in range(8)], "n": rng.randint(LOW, HIGH)}
