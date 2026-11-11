"""Maximum Price to Fill a Bag with 2 * 10^4 random items and a capacity just under their total
weight, so picking the best remaining ratio by a scan is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    items = [[rng.randint(1, 10**4), rng.randint(1, 10**4)] for _ in range(N)]
    capacity = max(1, sum(w for _, w in items) - rng.randint(1, 10**4))
    return {"items": items, "capacity": capacity}
