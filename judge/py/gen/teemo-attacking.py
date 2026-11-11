"""Teemo Attacking at the maximum 10^4 attacks: either every attack overlapping under a duration
of 10^7, so marking poisoned seconds one by one costs 10^11 steps, or thousands of separate
poison windows, so merging each attack into a list of windows is quadratic."""

SEEDS = 2
N = 10**4
TOP = 10**7


def generate(rng):
    if rng.random() < 0.5:
        # Random times under one huge duration: every attack overlaps the next.
        return {"timeSeries": sorted(rng.randint(0, TOP) for _ in range(N)), "duration": TOP}
    # Mostly gaps longer than the duration, some shorter or none: 8 * 10^3 or so windows, and
    # gaps of at most 2 * duration keep every time within 10^7.
    duration = rng.randint(TOP // (4 * N), TOP // (2 * N) - 1)
    times = [rng.randint(0, duration)]
    for _ in range(N - 1):
        if rng.random() < 0.8:
            gap = rng.randint(duration + 1, 2 * duration)
        else:
            gap = rng.randint(0, duration)
        times.append(times[-1] + gap)
    return {"timeSeries": times, "duration": duration}
