"""Minimum Obstacle Removal to Reach Corner on a 316 x 316 grid (about 10^5 cells) with 40%
obstacles, so Dijkstra that finds the next cell by scanning the open set is quadratic against
0-1 BFS."""

SEEDS = 2
M = 316
N = 316


def generate(rng):
    grid = [[1 if rng.random() < 0.4 else 0 for _ in range(N)] for _ in range(M)]
    grid[0][0] = grid[-1][-1] = 0
    return {"grid": grid}
