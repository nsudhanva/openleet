"""Latest Time to Catch a Bus at 10^5 buses and passengers: passengers on consecutive times so
every candidate slot is taken, or a random spread, punishing a per-minute search."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5
TOP = 10**9


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        base = rng.randint(2, 1000)
        passengers = list(range(base, base + N))
        buses = sorted(rng.sample(range(2, base + N + 1000), N))
        capacity = rng.randint(1, 3)
    elif shape == 1:
        passengers = rng.sample(range(2, TOP + 1), N)
        buses = rng.sample(range(2, TOP + 1), rng.randint(1, 100))
        capacity = rng.randint(N // 100, N)
    else:
        passengers = rng.sample(range(2, 3 * N), N)
        buses = rng.sample(range(2, TOP + 1), N)
        capacity = rng.randint(1, 10)
    rng.shuffle(passengers)
    rng.shuffle(buses)
    return {"buses": buses, "passengers": passengers, "capacity": capacity}
