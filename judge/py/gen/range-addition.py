"""Range Addition at the maximum length 10^5 with the maximum 10^4 updates, each spanning
about half the array, so applying them cell by cell does ~5 * 10^8 additions."""

SEEDS = 2
LENGTH = 10**5
UPDATES = 10**4


def generate(rng):
    updates = []
    for _ in range(UPDATES):
        a = rng.randrange(LENGTH // 2)
        b = rng.randrange(LENGTH // 2, LENGTH)
        updates.append([a, b, rng.randint(-1000, 1000)])
    return {"length": LENGTH, "updates": updates}
