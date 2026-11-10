"""Peak Index at n = 10^5: a strict mountain with the peak near one end, where a linear scan
from the wrong side walks almost the whole array."""

SEEDS = 2
N = 10**5


def generate(rng):
    peak = rng.choice([rng.randint(1, 50), rng.randint(N - 50, N - 2)])
    top = 10**6
    up = sorted(rng.sample(range(top), peak))
    down = sorted(rng.sample(range(top), N - 1 - peak), reverse=True)
    return {"arr": [*up, top, *down]}
