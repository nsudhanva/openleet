"""Number of Increasing Paths in a Grid on 150 by 150 or 60 by 400 cells whose values rise along
every row and column, so the number of paths is exponential and following each one without
memoization never finishes."""

SEEDS = 2


def generate(rng):
    m, n = (150, 150) if rng.random() < 0.5 else (60, 400)
    step = 10**5 // (m + n)
    return {
        "grid": [[(i + j) * step + rng.randrange(step) + 1 for j in range(n)] for i in range(m)]
    }
