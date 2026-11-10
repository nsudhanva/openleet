"""The Skyline Problem at 10^4 buildings sorted by left edge: deeply nested buildings, a dense
run where each building overlaps hundreds of others, or random spans up to 2^31 - 1."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
TOP = 2**31 - 1


def generate(rng):
    shape = pick_shape(rng)
    buildings = []
    if shape == 0:
        # Nested: each building inside the previous one but taller.
        for i in range(N):
            buildings.append([i, 2 * N - i, i + 1])
    elif shape == 1:
        # Dense overlap: every building spans up to 1000 later left edges.
        for i in range(N):
            left = i * 10
            buildings.append([left, left + rng.randint(10, 10**4), rng.randint(1, TOP)])
    else:
        for _ in range(N):
            left = rng.randint(0, TOP - 1)
            right = rng.randint(left + 1, min(TOP, left + 10**8))
            buildings.append([left, right, rng.randint(1, TOP)])
    buildings.sort(key=lambda b: b[0])
    return {"buildings": buildings}
