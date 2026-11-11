"""Minimum Moves to Balance Circular Array at n = 2 * 10^4: one debt nearly as large as everyone
else's small balances combined, so searching outward for the nearest donor afresh after each one
runs dry is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    balance = [rng.randint(0, 3) for _ in range(N)]
    i = rng.randrange(N)
    balance[i] = 0
    balance[i] = -(sum(balance) - rng.randint(0, 10))
    return {"balance": balance}
