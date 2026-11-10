"""Largest Plus Sign on a 500 x 500 grid with 5000 distinct mines, where scanning every arm
from every cell is cubic."""

SEEDS = 2
N = 500
MINES = 5000


def generate(rng):
    n = N
    if rng.random() < 0.5:
        cells = rng.sample(range(n * n), MINES)
    else:
        # Mines packed along a few rows and columns, leaving large open blocks.
        chosen = set()
        lines = rng.sample(range(n), 10)
        while len(chosen) < MINES:
            if rng.random() < 0.5:
                cell = rng.choice(lines) * n + rng.randrange(n)
            else:
                cell = rng.randrange(n) * n + rng.choice(lines)
            chosen.add(cell)
        cells = sorted(chosen)
        rng.shuffle(cells)
    return {"n": n, "mines": [[c // n, c % n] for c in cells]}
