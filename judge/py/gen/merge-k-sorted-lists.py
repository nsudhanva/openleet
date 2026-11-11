"""Merge k Sorted Lists with the maximum 10^4 nodes, one per list, rising from each list to the next
on one seed and falling on the other, so folding the lists in one at a time from either end walks
the whole result every time on some seed (~5 * 10^7 steps), as does scanning every head."""

SEEDS = 2
TOTAL = 10**4
LIMIT = 10**4


def generate(rng):
    if rng.random() < 0.5:
        values = sorted(rng.randint(-LIMIT, LIMIT) for _ in range(TOTAL))
        return {"lists": [[v] for v in values]}
    # Falling, with few distinct values (long runs of ties) and some empty lists in between.
    empty = rng.randint(1, 50)
    values = sorted((rng.randint(-100, 100) for _ in range(TOTAL - empty)), reverse=True)
    lists = [[v] for v in values]
    for _ in range(empty):
        lists.insert(rng.randrange(len(lists) + 1), [])
    return {"lists": lists}
