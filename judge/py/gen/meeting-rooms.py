"""Meeting Rooms at the maximum 10^4 shuffled meetings that never overlap (or overlap only in the
last pair), so comparing every pair costs ~5 * 10^7 checks."""

SEEDS = 2
N = 10**4
LIMIT = 10**6


def generate(rng):
    points = sorted(rng.sample(range(LIMIT + 1), 2 * N))
    intervals = [[points[2 * i], points[2 * i + 1]] for i in range(N)]
    rng.shuffle(intervals)
    if rng.random() < 0.5:
        intervals[-1] = list(intervals[-2])
    return {"intervals": intervals}
