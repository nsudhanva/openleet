"""Painting the Walls at the maximum 500 walls, three quarters taking 450 to 500 time units and
the rest quick and cheap, so a subset search explodes and a knapsack over the total time does
~10^8 steps where the O(n^2) DP does ~2.5 * 10^5."""

SEEDS = 2
N = 500


def generate(rng):
    time = [rng.randint(450, 500) if rng.random() < 0.75 else rng.randint(1, 10) for _ in range(N)]
    cost = [min(10**6, t * rng.randint(500, 2000)) for t in time]
    return {"cost": cost, "time": time}
