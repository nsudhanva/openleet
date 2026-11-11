"""Put Boxes Into the Warehouse II with 3 * 10^4 boxes and 3 * 10^4 rooms, low in the middle and
tall at both ends, so searching every room for the best fit of each box does ~9 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
M = 3 * 10**4


def generate(rng):
    warehouse = [rng.randint(1, 10**9) for _ in range(N)]
    warehouse[: N // 4] = sorted(warehouse[: N // 4], reverse=True)
    warehouse[-(N // 4) :] = sorted(warehouse[-(N // 4) :])
    boxes = [rng.randint(1, 10**9) for _ in range(M)]
    return {"boxes": boxes, "warehouse": warehouse}
