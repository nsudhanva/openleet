"""Minimum Moves to Equal Array Elements at n = 10^5 with values near +-10^9 but an answer
that fits in 32 bits; simulating the moves one at a time is hopeless."""

SEEDS = 3
N = 10**5
SPREAD = 20000


def generate(rng):
    base = rng.choice((-(10**9), 10**9 - SPREAD, rng.randint(-(10**9), 10**9 - SPREAD)))
    return {"nums": [base + rng.randint(0, SPREAD) for _ in range(N)]}
