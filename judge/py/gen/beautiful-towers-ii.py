"""Beautiful Towers II at n = 10^4 random heights up to 10^9, so spreading out from every peak
is ~10^8 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    top = rng.choice([10**9, 10**3])
    return {"maxHeights": [rng.randint(1, top) for _ in range(N)]}
