"""Maximum Score of Non-overlapping Intervals at n = 5 * 10^4: one seed with wide random
weights, one with weights from a tiny set so many choices tie and the lexicographically
smallest index list must be found."""

SEEDS = 3
N = 5 * 10**4
TOP = 10**9


def generate(rng):
    small = rng.random() < 0.5
    span = rng.choice((10**4, 10**7))
    intervals = []
    for _ in range(N):
        left = rng.randint(1, TOP)
        right = rng.randint(left, min(TOP, left + span))
        weight = rng.randint(1, 3) if small else rng.randint(1, 10**9)
        intervals.append([left, right, weight])
    return {"intervals": intervals}
