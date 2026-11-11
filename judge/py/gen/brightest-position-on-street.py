"""Brightest Position on the Street at 10^4 lamps with wide, heavily overlapping ranges, so
counting the lamps over every candidate position is quadratic."""

SEEDS = 2
N = 10**4
LIMIT = 10**8


def generate(rng):
    lights = []
    for _ in range(N):
        pos = rng.randint(-LIMIT, LIMIT)
        lights.append([pos, rng.randint(0, LIMIT // rng.choice((1, 10, 1000)))])
    return {"lights": lights}
