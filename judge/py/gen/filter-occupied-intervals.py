"""Filter Occupied Intervals with the maximum 5 * 10^4 intervals, all separate and listed in
descending order, so merging each one into the result by scanning it (or splicing it into sorted
lists) is ~10^9 steps (~10^9 element moves)."""

SEEDS = 2
N = 5 * 10**4
TOP = 10**7


def generate(rng):
    # Even endpoints keep the intervals at least one unoccupied point apart, so none touch;
    # endpoints below 10^7 keep the JSON under 1 MB.
    ends = sorted((2 * v for v in rng.sample(range(1, TOP // 2), 2 * N)), reverse=True)
    intervals = [[ends[2 * i + 1], ends[2 * i]] for i in range(N)]
    lo = rng.randint(TOP // 4, TOP // 2)
    return {
        "occupiedIntervals": intervals,
        "freeStart": lo,
        "freeEnd": lo + rng.randint(1, TOP // 4),
    }
