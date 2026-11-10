"""Cherry Pickup at the maximum 50 x 50: mostly cherries with scattered thorns (the O(n^3) DP
runs fully), or no thorns at all."""

SEEDS = 3
N = 50


def generate(rng):
    thorn = rng.choice([0.0, 0.1, 0.25])
    grid = [
        [-1 if rng.random() < thorn else rng.choice([0, 1, 1]) for _ in range(N)] for _ in range(N)
    ]
    grid[0][0] = rng.randint(0, 1)
    grid[N - 1][N - 1] = rng.randint(0, 1)
    return {"grid": grid}
