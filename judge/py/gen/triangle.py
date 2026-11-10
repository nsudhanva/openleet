"""Triangle at the maximum 200 rows with values in [-10^4, 10^4], where plain recursion over
all 2^199 paths is hopeless."""

SEEDS = 2
ROWS = 200


def generate(rng):
    return {"triangle": [[rng.randint(-(10**4), 10**4) for _ in range(r + 1)] for r in range(ROWS)]}
