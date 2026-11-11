"""Find Kth Largest XOR Coordinate Value on a 1000 by 250 matrix (transposed on one seed) of values
below 100, so XOR-ing each coordinate's rectangle from scratch is ~10^10 steps and its column (or
row) of row prefixes ~10^8."""

SEEDS = 2
M, N = 1000, 250
TOP = 99


def generate(rng):
    m, n = (N, M) if rng.random() < 0.5 else (M, N)
    matrix = [[rng.randint(0, TOP) for _ in range(n)] for _ in range(m)]
    return {"matrix": matrix, "k": rng.randint(1, m * n)}
