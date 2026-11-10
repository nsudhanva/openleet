"""Cut Off Trees on a 50 x 50 forest with hundreds of distinct-height trees scattered so
consecutive trees are far apart, each needing its own BFS."""

SEEDS = 2
M = N = 50


def generate(rng):
    obstacles = rng.choice([0.0, 0.1])
    tree_p = rng.uniform(0.2, 0.35)
    cells = []
    for r in range(M):
        row = []
        for c in range(N):
            x = rng.random()
            if (r, c) != (0, 0) and x < obstacles:
                row.append(0)
            elif x < obstacles + tree_p:
                row.append(-1)
            else:
                row.append(1)
        cells.append(row)
    spots = [(r, c) for r in range(M) for c in range(N) if cells[r][c] == -1]
    if not spots:
        cells[M - 1][N - 1] = -1
        spots = [(M - 1, N - 1)]
    heights = rng.sample(range(2, 10**9 + 1), len(spots))
    for (r, c), h in zip(spots, heights, strict=True):
        cells[r][c] = h
    return {"forest": cells}
