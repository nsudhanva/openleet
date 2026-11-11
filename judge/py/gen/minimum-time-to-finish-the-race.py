"""Minimum Time to Finish the Race at 10^5 tires and 1000 laps, with changeTime 10^5 and small f
so each tire stays worth keeping for ~17 laps; costing every tire for every lap count up to
numLaps is ~10^8 steps on numbers that grow past r^1000."""

SEEDS = 2
N = 10**5
LAPS = 1000


def generate(rng):
    tires = [[rng.randint(1, 100), rng.randint(2, 4)] for _ in range(N)]
    return {"tires": tires, "changeTime": 10**5 - rng.randrange(100), "numLaps": LAPS}
