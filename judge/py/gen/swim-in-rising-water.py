"""Swim in Rising Water on the maximum 50 x 50 grid: a random permutation, or a low-valued
serpentine path among high walls so the answer path is 1,250 cells long."""

SEEDS = 3
N = 50


def generate(rng):
    cells = N * N
    if rng.random() < 0.5:
        values = list(range(cells))
        rng.shuffle(values)
        return {"grid": [values[r * N : (r + 1) * N] for r in range(N)]}
    path = []
    for r in range(0, N, 2):
        cols = range(N) if (r // 2) % 2 == 0 else range(N - 1, -1, -1)
        path.extend((r, c) for c in cols)
        if r + 1 < N:
            path.append((r + 1, N - 1 if (r // 2) % 2 == 0 else 0))
    on_path = set(path)
    grid = [[0] * N for _ in range(N)]
    low = list(range(len(path)))
    rng.shuffle(low)
    for (r, c), v in zip(path, low, strict=True):
        grid[r][c] = v
    rest = [(r, c) for r in range(N) for c in range(N) if (r, c) not in on_path]
    high = list(range(len(path), cells))
    rng.shuffle(high)
    for (r, c), v in zip(rest, high, strict=True):
        grid[r][c] = v
    return {"grid": grid}
