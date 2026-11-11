"""Beautiful Towers I at n = 10^3 random heights up to 10^9, so recomputing each tower's cap as
a range minimum for every peak is ~3 * 10^8 steps."""

SEEDS = 2
N = 10**3


def generate(rng):
    top = rng.choice([10**9, 10**3])
    return {"heights": [rng.randint(1, top) for _ in range(N)]}
