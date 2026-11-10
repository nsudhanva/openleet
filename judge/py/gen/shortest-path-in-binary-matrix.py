"""Shortest Path in Binary Matrix on a 100 x 100 grid: open with sparse walls, or a serpentine
maze forcing a very long path."""

SEEDS = 3
N = 100


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        grid = [[1 if rng.random() < 0.2 else 0 for _ in range(N)] for _ in range(N)]
        grid[0][0] = grid[N - 1][N - 1] = 0
    elif shape == 1:
        # Walls on every other row with a single gap alternating sides.
        grid = [[0] * N for _ in range(N)]
        for r in range(1, N - 1, 2):
            gap = N - 1 if (r // 2) % 2 == 0 else 0
            for c in range(N):
                if c != gap:
                    grid[r][c] = 1
    else:
        grid = [[1 if rng.random() < 0.4 else 0 for _ in range(N)] for _ in range(N)]
    return {"grid": grid}
