"""Minimum Path Sum on the largest 200 x 200 grid, values in [0, 200]."""

SEEDS = 2


def generate(rng):
    rows = rng.choice((200, rng.randint(1, 200)))
    return {"grid": [[rng.randint(0, 200) for _ in range(200)] for _ in range(rows)]}
