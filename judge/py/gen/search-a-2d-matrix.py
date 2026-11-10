"""Search a 2D Matrix on a 100 x 100 strictly increasing matrix (row-major), target present or
absent."""

SEEDS = 3


def generate(rng):
    m, n = 100, 100
    values = sorted(rng.sample(range(-(10**4), 10**4 + 1), m * n))
    matrix = [values[i * n : (i + 1) * n] for i in range(m)]
    present = set(values)
    if rng.random() < 0.5:
        target = rng.choice(values)
    else:
        target = rng.choice([v for v in range(-(10**4), 10**4 + 1) if v not in present])
    return {"matrix": matrix, "target": target}
