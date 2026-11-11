"""Painting the Walls at the maximum 500 walls, 95% taking 480 to 500 time units and the
rest quick and cheap, so a subset search explodes and a knapsack over the total time (~2.4 * 10^5)
does ~6 * 10^7 steps per seed where the O(n^2) DP does ~2.5 * 10^5."""

SEEDS = 3
N = 500


def generate(rng):
    time = [rng.randint(480, 500) if rng.random() < 0.95 else rng.randint(1, 10) for _ in range(N)]
    cost = [min(10**6, t * rng.randint(500, 2000)) for t in time]
    return {"cost": cost, "time": time}
