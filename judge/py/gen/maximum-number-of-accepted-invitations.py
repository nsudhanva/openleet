"""Maximum Number of Accepted Invitations on a 200 x 200 grid with a few invitations per boy and
no perfect matching, so searching every assignment cannot finish."""

SEEDS = 2
M = N = 200


def generate(rng):
    # Girls 0..N/4 are popular; the rest each get few invitations, so some boys go unmatched.
    grid = [[0] * N for _ in range(M)]
    for i in range(M):
        for _ in range(rng.randint(1, 4)):
            j = rng.randrange(N // 4) if rng.random() < 0.6 else rng.randrange(N)
            grid[i][j] = 1
    return {"grid": grid}
