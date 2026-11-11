"""Put Boxes Into the Warehouse I with 3 * 10^4 boxes and 3 * 10^4 tall rooms, nearly every box
fitting, so walking each box in from the entrance to the deepest free room does ~4.5 * 10^8
steps."""

SEEDS = 2
N = 3 * 10**4
M = 3 * 10**4


def generate(rng):
    warehouse = [rng.randint(5 * 10**8, 10**9) for _ in range(N)]
    for _ in range(20):
        warehouse[rng.randrange(N // 2, N)] = rng.randint(1, 10**9)
    boxes = [rng.randint(1, 6 * 10**8) for _ in range(M)]
    return {"boxes": boxes, "warehouse": warehouse}
