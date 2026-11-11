"""Minimum Time to Finish the Race at 10^5 tires (about 10^5 distinct) and 1000 laps, with
changeTime 10^5: 1000 tires have small f and r in 2..4, so each stays worth keeping for ~17 laps,
and the rest are random over the full range. Costing every distinct tire for every lap count up
to numLaps is ~10^8 steps on numbers that grow past r^1000, and deduplicating does not help."""

SEEDS = 2
N = 10**5
LAPS = 1000
GOOD = 1000


def generate(rng):
    tires = [[rng.randint(1, 100), rng.randint(2, 4)] for _ in range(GOOD)]
    tires += [[rng.randint(1, 10**5), rng.randint(2, 10**5)] for _ in range(N - GOOD)]
    rng.shuffle(tires)
    return {"tires": tires, "changeTime": 10**5 - rng.randrange(100), "numLaps": LAPS}
