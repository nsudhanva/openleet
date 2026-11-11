"""Number of Islands II at the maximum 10^4 cells and 10^4 additions (every cell once, or random
cells with repeats), so recounting the islands with a flood fill after each addition costs
~5 * 10^7 steps."""

SEEDS = 2
CELLS = 10**4


def generate(rng):
    if rng.random() < 0.5:
        m = n = 100
        positions = [[i, j] for i in range(m) for j in range(n)]
        rng.shuffle(positions)
    else:
        m, n = 50, CELLS // 50
        positions = [[rng.randrange(m), rng.randrange(n)] for _ in range(CELLS)]
    return {"m": m, "n": n, "positions": positions}
