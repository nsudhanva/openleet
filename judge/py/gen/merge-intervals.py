"""Merge Intervals at the maximum n = 10^4 over [0, 10^4], shuffled, mostly single points or
length-1 intervals so thousands of intervals stay separate: merging each one into an unsorted
result by scanning it is ~3 * 10^7 comparisons."""

SEEDS = 2
N = 10**4
TOP = 10**4


def generate(rng):
    if rng.random() < 0.5:
        # Distinct points with a few short intervals that join neighbours.
        intervals = [[a, a] for a in rng.sample(range(TOP + 1), N)]
        for iv in rng.sample(intervals, N // 20):
            iv[1] = min(TOP, iv[0] + rng.randint(1, 3))
    else:
        # Disjoint pairs [2i, 2i + 1], each split into pieces and copies that merge back.
        intervals = []
        while len(intervals) < N:
            a = 2 * rng.randrange(TOP // 2)
            intervals.append(rng.choice([[a, a + 1], [a, a], [a + 1, a + 1]]))
    rng.shuffle(intervals)
    return {"intervals": intervals}
