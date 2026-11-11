"""Largest Values From Labels at n = 2 * 10^4 with 2,000 labels, useLimit 5 and numWanted = n, so
picking the best remaining item by a fresh scan ~10^4 times costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LABELS = 2000
USE = 5


def generate(rng):
    values = [rng.randint(0, 2 * 10**4) for _ in range(N)]
    labels = [rng.randrange(LABELS) for _ in range(N)]
    return {"values": values, "labels": labels, "numWanted": N, "useLimit": USE}
