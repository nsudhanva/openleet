"""Find Right Interval with 2 * 10^4 intervals, unique starts over [-10^6, 10^6], lengths from
zero to huge so many have no right interval."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    starts = rng.sample(range(-(10**6), 10**6 + 1), N)
    long = rng.random() < 0.5
    intervals = []
    for s in starts:
        span = rng.randint(0, 10**6 if long else 200)
        intervals.append([s, min(10**6, s + span)])
    return {"intervals": intervals}
