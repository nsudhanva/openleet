"""Teemo Attacking at 10^4 attacks with durations up to 10^7: heavy overlap, repeated times,
or widely spaced, punishing per-second simulation."""

SEEDS = 3
N = 10**4
TOP = 10**7


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        times = sorted(rng.randint(0, TOP) for _ in range(N))
        duration = TOP
    elif shape == 1:
        times = sorted(rng.randint(0, 2000) for _ in range(N))  # many equal times
        duration = rng.randint(0, 5)
    else:
        times = sorted(rng.randint(0, TOP) for _ in range(N))
        duration = rng.randint(0, 2000)
    return {"timeSeries": times, "duration": duration}
