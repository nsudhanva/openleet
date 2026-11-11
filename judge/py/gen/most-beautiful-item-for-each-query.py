"""Most Beautiful Item for Each Query at 5 * 10^4 items and 5 * 10^4 queries. One shape has beauty
rising with price, so a scan from the most beautiful item must pass every dearer item before it
finds one a query affords; the other has random prices and beauties. Scanning every item for every
query, or scanning in beauty order on the first shape, is ~10^9 steps."""

from _shapes import pick_shape

SEEDS = 2
N = 5 * 10**4
TOP = 10**9


def generate(rng):
    shape = pick_shape(rng)
    items = []
    for _ in range(N):
        price = rng.randint(1, TOP)
        beauty = min(TOP, price + rng.randint(0, 10**6)) if shape == 0 else rng.randint(1, TOP)
        items.append([price, beauty])
    return {"items": items, "queries": [rng.randint(1, TOP) for _ in range(N)]}
