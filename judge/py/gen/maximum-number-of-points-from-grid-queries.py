"""Maximum Number of Points From Grid Queries on a 300 x 300 grid with a low start cell and 10^4
mostly large queries, so a flood fill or a linear count per query is quadratic."""

SEEDS = 2
M = N = 300
K = 10**4


def generate(rng):
    grid = [[rng.randint(1, 10**6) for _ in range(N)] for _ in range(M)]
    grid[0][0] = 1
    queries = [
        rng.randint(1, 10**6) if rng.random() < 0.2 else rng.randint(6 * 10**5, 10**6)
        for _ in range(K)
    ]
    return {"grid": grid, "queries": queries}
