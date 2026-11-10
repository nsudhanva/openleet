"""Merge k Sorted Lists with 10^4 total nodes: 10^4 single-node lists (k at the maximum) or
20 lists of 500, so merging one list at a time is quadratic."""

SEEDS = 3
TOTAL = 10**4


def generate(rng):
    k = rng.choice((TOTAL, 20, 2000))
    size = TOTAL // k
    lists = [sorted(rng.randint(-(10**4), 10**4) for _ in range(size)) for _ in range(k)]
    if k == 2000:
        lists[rng.randrange(k)] = []
    return {"lists": lists}
