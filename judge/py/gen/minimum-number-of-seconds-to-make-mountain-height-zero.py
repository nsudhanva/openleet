"""Minimum Number of Seconds to Make Mountain Height Zero with height 10^5 and 2000 workers, so
handing out the height one unit at a time to the worker who would finish it first, found by a
scan, costs 2 * 10^8 steps."""

SEEDS = 2
HEIGHT = 10**5
WORKERS = 2000
LIMIT = 10**6


def generate(rng):
    return {
        "mountainHeight": HEIGHT,
        "workerTimes": [rng.randint(1, LIMIT) for _ in range(WORKERS)],
    }
