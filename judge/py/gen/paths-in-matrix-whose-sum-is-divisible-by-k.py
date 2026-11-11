"""Paths in Matrix Whose Sum Is Divisible by K on a 100 x 100 grid with k in [20, 30], so a DP
keeping every distinct path sum (up to ~2 * 10^4 per cell) does ~10^8 steps where keeping sums
mod k does ~3 * 10^5."""

SEEDS = 2
M = 100
N = 100


def generate(rng):
    grid = [[rng.randint(0, 100) for _ in range(N)] for _ in range(M)]
    return {"grid": grid, "k": rng.randint(20, 30)}
