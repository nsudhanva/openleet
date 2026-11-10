"""Insert Interval with 10^4 sorted, non-overlapping intervals over [0, 10^5] and a new interval
that swallows a long stretch, touches endpoints exactly, or lands past the end."""

SEEDS = 3
N = 10**4
HI = 10**5


def generate(rng):
    points = sorted(rng.sample(range(HI + 1), 2 * N))
    intervals = [[points[2 * i], points[2 * i + 1]] for i in range(N)]
    shape = rng.randrange(3)
    if shape == 0:
        a, b = sorted(rng.sample(range(HI + 1), 2))
    elif shape == 1:
        i, j = sorted(rng.sample(range(N), 2))
        a, b = intervals[i][1], intervals[j][0]
    else:
        a = b = rng.choice([HI, 0, intervals[-1][1]])
    return {"intervals": intervals, "newInterval": [a, b]}
