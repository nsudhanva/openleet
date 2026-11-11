"""Grid Game at n = 3 * 10^4 columns, so re-summing both rows for each turning column costs
~9 * 10^8 additions."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    return {"grid": [[rng.randint(1, 10**5) for _ in range(N)] for _ in range(2)]}
