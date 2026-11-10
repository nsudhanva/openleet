"""Gas Station at n = 10^5: total gas just covers total cost and exactly one start works (found
far from the front), or total gas falls just short."""

SEEDS = 3
N = 10**5


def valid_starts(gas, cost):
    d = [g - c for g, c in zip(gas, cost, strict=False)]
    total = sum(d)
    if total < 0:
        return []
    prefix, run = [], 0
    for x in d:
        run += x
        prefix.append(run)
    suffix_min = prefix[:]
    for i in range(N - 2, -1, -1):
        suffix_min[i] = min(suffix_min[i], suffix_min[i + 1])
    starts, before, low = [], 0, float("inf")  # low = min prefix over [0, s - 1]
    for s in range(N):
        if suffix_min[s] - before >= 0 and total + low - before >= 0:
            starts.append(s)
        before = prefix[s]
        low = min(low, prefix[s])
    return starts


def generate(rng):
    short = rng.random() < 0.34
    while True:
        gas = [rng.randint(0, 10**4) for _ in range(N)]
        cost = [rng.randint(0, 10**4) for _ in range(N)]
        gap = sum(cost) - sum(gas) + (-1 if short else rng.choice([0, 5]))
        # Move gas totals toward cost totals one station at a time.
        while gap != 0:
            i = rng.randrange(N)
            step = max(-gas[i], min(10**4 - gas[i], gap))
            gas[i] += step
            gap -= step
        if short or len(valid_starts(gas, cost)) == 1:
            return {"gas": gas, "cost": cost}
