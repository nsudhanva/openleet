"""Range Addition II with m, n = 4 * 10^4 and 10^4 operations, so materializing the matrix is
hopeless."""

SEEDS = 2
TOP = 4 * 10**4
OPS = 10**4


def generate(rng):
    m, n = TOP, rng.randint(3 * TOP // 4, TOP)
    ops = [[rng.randint(m // 2, m), rng.randint(n // 2, n)] for _ in range(OPS)]
    return {"m": m, "n": n, "ops": ops}
