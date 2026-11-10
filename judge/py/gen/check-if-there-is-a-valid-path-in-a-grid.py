"""Valid Path in a Grid at 299 x 300: a snake of streets through every cell from the top-left to
the bottom-right (true, the walk visits all ~9 * 10^4 cells), the same with one cell broken
(false), or random streets."""

SEEDS = 3
M, N = 299, 300


def generate(rng):
    shape = rng.choice(["snake", "broken", "random"])
    if shape == "random":
        return {"grid": [[rng.randint(1, 6) for _ in range(N)] for _ in range(M)]}
    grid = [[1] * N for _ in range(M)]
    for r in range(M):
        if r % 2 == 0:
            if r > 0:
                grid[r][0] = 6  # from above, out to the right
            if r < M - 1:
                grid[r][N - 1] = 3  # from the left, down
        else:
            grid[r][N - 1] = 5  # from above, out to the left
            grid[r][0] = 4  # from the right, down
    if shape == "broken":
        r = rng.randrange(M // 4, 3 * M // 4)
        c = rng.randrange(1, N - 1)
        grid[r][c] = 2  # an up-down street across a left-right corridor breaks the snake
    return {"grid": grid}
