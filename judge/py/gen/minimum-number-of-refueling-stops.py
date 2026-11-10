"""Minimum Number of Refueling Stops with the maximum 500 stations toward a target of up to
10^9, fuel sized so the car needs many stops (or cannot make it)."""

SEEDS = 3
STATIONS = 500


def generate(rng):
    target = rng.choice((10**9, rng.randint(10**6, 10**9)))
    positions = sorted(rng.sample(range(1, target), STATIONS))
    gap = target // STATIONS
    fuel = [rng.randint(1, 3 * gap) for _ in range(STATIONS)]
    start = positions[0] + rng.randint(0, 2 * gap)
    stations = [[p, f] for p, f in zip(positions, fuel, strict=True)]
    return {"target": target, "startFuel": min(start, 10**9), "stations": stations}
