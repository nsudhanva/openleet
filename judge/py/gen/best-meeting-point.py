"""Best Meeting Point on a 200 x 200 grid with 80% or 95% of the cells homes, so summing every
friend's distance to every cell is ~1.5 * 10^9 steps."""

SEEDS = 2
N = 200


def generate(rng):
    p = rng.choice([0.95, 0.8])
    grid = [[int(rng.random() < p) for _ in range(N)] for _ in range(N)]
    grid[0][0] = grid[N - 1][N - 1] = 1
    return {"grid": grid}
