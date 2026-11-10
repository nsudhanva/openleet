"""Remove Covered Intervals with 1000 unique intervals: nested chains with shared endpoints,
or random ones, so a pairwise check does a million comparisons."""

SEEDS = 2


def generate(rng):
    seen = set()
    nested = rng.random() < 0.5
    while len(seen) < 1000:
        if nested:
            lo = rng.randint(0, 500)
            hi = rng.randint(10**5 - 500, 10**5)
            if rng.random() < 0.3:
                lo = 0
        else:
            lo = rng.randint(0, 10**5 - 1)
            hi = rng.randint(lo + 1, min(10**5, lo + 20000))
        seen.add((lo, hi))
    intervals = [list(p) for p in sorted(seen)]
    rng.shuffle(intervals)
    return {"intervals": intervals}
