"""Maximum Number of Points with Cost on a 4 x 10^4 matrix, so trying every previous column for
each cell is quadratic in the row width."""

SEEDS = 2
M, N = 4, 10**4


def generate(rng):
    return {"points": [[rng.randint(0, 10**5) for _ in range(N)] for _ in range(M)]}
