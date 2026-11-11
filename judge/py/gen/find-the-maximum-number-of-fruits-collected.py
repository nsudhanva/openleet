"""Find the Maximum Number of Fruits Collected on a 100 x 100 grid, so following each child's
moves without memoizing is 3^99 paths while the DP is 10^4 cells."""

SEEDS = 2
N = 100


def generate(rng):
    top = rng.choice((1000, 3))
    return {"fruits": [[rng.randint(0, top) for _ in range(N)] for _ in range(N)]}
