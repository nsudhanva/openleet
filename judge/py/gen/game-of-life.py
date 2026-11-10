"""Game of Life on the maximum 25 x 25 board, random density or a glider-gun-like dense block."""

SEEDS = 2


def generate(rng):
    m, n = rng.choice([(25, 25), (25, 13)])
    p = rng.choice([0.3, 0.6])
    return {"board": [[1 if rng.random() < p else 0 for _ in range(n)] for _ in range(m)]}
