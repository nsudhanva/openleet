"""Maximum Number of Moves in a Grid on a 1000 x 100 grid that rises column by column, with a wall
of 1s a few columns before the end, so following each path without memoising, or once per start
row, cannot finish."""

SEEDS = 2
M, N = 1000, 100


def generate(rng):
    wall = N - rng.randint(2, 5)
    grid = [
        [1 if j == wall else 1000 * j + rng.randint(1, 1200) for j in range(N)] for _ in range(M)
    ]
    return {"grid": grid}
