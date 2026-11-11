"""Cutting Ribbons with 2 * 10^4 ribbons up to 10^5: an answer near 5 * 10^4, so trying lengths one
by one from either end costs ~10^9 steps, or an answer under 50 (k ~ 10^8), so popping the longest
piece k times from a heap does too."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
TOP = 10**5


def generate(rng):
    ribbons = [rng.randint(1, TOP) for _ in range(N)]
    x = rng.randint(10, 50) if pick_shape(rng) == 2 else rng.randint(TOP * 2 // 5, TOP * 3 // 5)
    return {"ribbons": ribbons, "k": sum(r // x for r in ribbons)}
