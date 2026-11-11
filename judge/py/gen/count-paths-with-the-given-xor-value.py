"""Count Paths With the Given XOR Value on a 30 x 30 grid, so enumerating its ~3 * 10^16
monotone paths is hopeless while the DP has 14,400 states."""

SEEDS = 2
M = N = 30


def generate(rng):
    grid = [[rng.randrange(16) for _ in range(N)] for _ in range(M)]
    return {"grid": grid, "k": rng.randrange(16)}
