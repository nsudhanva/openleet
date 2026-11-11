"""Minimum White Tiles at floor length 1000 (about 60% white) with 100 carpets of length 3, so
covering less than the floor, a DP that tries every next carpet position from every state is
~10^8 steps."""

SEEDS = 2
N = 1000
CARPETS = 100
LENGTH = 3


def generate(rng):
    floor = "".join("1" if rng.random() < 0.6 else "0" for _ in range(N))
    return {"floor": floor, "numCarpets": CARPETS, "carpetLen": LENGTH}
