"""Shortest Distance from All Buildings on a 50 x 50 grid with only one to three buildings and a few
obstacles, so a BFS from every empty cell (~2400 of them) does ~1000x the per-building BFS work."""

SEEDS = 2
M = N = 50


def generate(rng):
    grid = [[2 if rng.random() < 0.05 else 0 for _ in range(N)] for _ in range(M)]
    for _ in range(rng.randint(1, 3)):
        grid[rng.randrange(M)][rng.randrange(N)] = 1
    return {"grid": grid}
