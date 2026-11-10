"""01 Matrix at m * n = 10^4: a single 0 in a corner (distances up to ~200), a sparse random
grid, or a 1 x 10^4 row with one 0, all punishing a BFS-per-cell approach."""

SEEDS = 3


def generate(rng):
    shape = rng.choice(["corner", "sparse", "row"])
    if shape == "row":
        mat = [[1] * 10**4]
        mat[0][rng.randrange(10**4)] = 0
        return {"mat": mat}
    if shape == "corner":
        m = n = 100
        mat = [[1] * n for _ in range(m)]
        mat[rng.choice([0, m - 1])][rng.choice([0, n - 1])] = 0
        return {"mat": mat}
    m = rng.choice([50, 100, 200])
    n = 10**4 // m
    mat = [[0 if rng.random() < 0.002 else 1 for _ in range(n)] for _ in range(m)]
    mat[rng.randrange(m)][rng.randrange(n)] = 0
    return {"mat": mat}
