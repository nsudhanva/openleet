"""Earliest Moment Everyone Becomes Friends with n = 100 and every one of the 4950 pairs
logged in random time order (unsorted), or with one person never connected."""

from _shapes import pick_shape

SEEDS = 3
N = 100


def generate(rng):
    shape = pick_shape(rng)
    loner = rng.randrange(N) if shape == 2 else -1
    pairs = [[x, y] for x in range(N) for y in range(x + 1, N) if loner not in (x, y)]
    rng.shuffle(pairs)
    if shape == 1:
        pairs = pairs[: rng.randint(500, len(pairs))]
    times = rng.sample(range(10**9 + 1), len(pairs))
    logs = []
    for (x, y), t in zip(pairs, times, strict=True):
        logs.append([t, x, y] if rng.random() < 0.5 else [t, y, x])
    return {"logs": logs, "n": N}
