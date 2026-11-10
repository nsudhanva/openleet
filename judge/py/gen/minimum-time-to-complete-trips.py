"""Minimum Time to Complete Trips with 10^5 buses and up to 10^7 trips at times up to 10^7,
so the answer reaches ~10^14 and stepping through time is hopeless."""

SEEDS = 3
N = 10**5


def generate(rng):
    n = rng.choice((N, 1))
    slow = rng.random() < 0.5
    time = [rng.randint(10**6 if slow else 1, 10**7) for _ in range(n)]
    return {"time": time, "totalTrips": rng.choice((10**7, rng.randint(1, 10**7)))}
