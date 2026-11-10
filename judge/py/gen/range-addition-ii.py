"""Range Addition II with m, n = 4 * 10^4 and 10^4 operations, so materializing the matrix is
hopeless."""

SEEDS = 2


def generate(rng):
    m, n = 4 * 10**4, rng.randint(3 * 10**4, 4 * 10**4)
    ops = [[rng.randint(m // 2, m), rng.randint(n // 2, n)] for _ in range(10**4)]
    return {"m": m, "n": n, "ops": ops}
