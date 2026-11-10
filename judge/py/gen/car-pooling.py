"""Car Pooling at the maximum 1000 trips over stops 0..1000: overlapping long trips with the
capacity set right at, or just below, the peak load."""

SEEDS = 3


def generate(rng):
    trips = []
    for _ in range(1000):
        a = rng.randint(0, 999)
        b = rng.randint(a + 1, 1000)
        trips.append([rng.randint(1, 100), a, b])
    load = [0] * 1002
    for p, a, b in trips:
        load[a] += p
        load[b] -= p
    peak, cur = 0, 0
    for v in load:
        cur += v
        peak = max(peak, cur)
    capacity = max(1, min(10**5, peak + rng.choice([0, -1, 1])))
    return {"trips": trips, "capacity": capacity}
