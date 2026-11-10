"""Find Missing and Repeated Values on a 50 x 50 grid: a shuffled 1..2500 with one value replaced
by another."""

SEEDS = 2
N = 50


def generate(rng):
    values = list(range(1, N * N + 1))
    rng.shuffle(values)
    i, j = rng.sample(range(N * N), 2)
    values[i] = values[j]
    return {"grid": [values[r * N : (r + 1) * N] for r in range(N)]}
