"""Max Area of Island on a 50 x 50 grid: one snake-shaped island covering most cells (deep
DFS), or random cells."""

SEEDS = 2
N = 50


def generate(rng):
    if rng.random() < 0.5:
        grid = [[0] * N for _ in range(N)]
        for r in range(N):
            if r % 2 == 0:
                grid[r] = [1] * N
            else:
                grid[r][N - 1 if r % 4 == 1 else 0] = 1
        return {"grid": grid}
    return {"grid": [[rng.randint(0, 1) for _ in range(N)] for _ in range(N)]}
