"""Maximum Profit in Job Scheduling at n = 5 * 10^4 jobs: short jobs scattered over
[1, 10^9] in one seed, heavily overlapping long jobs in the other."""

SEEDS = 3
N = 5 * 10**4
TOP = 10**9


def generate(rng):
    span = rng.choice((10**5, TOP // 2))
    start, end, profit = [], [], []
    for _ in range(N):
        s = rng.randint(1, TOP - 1)
        e = rng.randint(s + 1, min(TOP, s + span))
        start.append(s)
        end.append(e)
        profit.append(rng.randint(1, 10**4))
    return {"startTime": start, "endTime": end, "profit": profit}
