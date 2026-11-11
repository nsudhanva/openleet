"""Shortest Distance to Target Color with 5 * 10^4 colors and queries: color 3 sits only at the
two ends (seeds 0 and 2) or nowhere (seed 1) and almost every query asks for it, so scanning
outward per query, even with C-speed list.index, is ~n steps each, ~2.5 * 10^9 over a seed."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4
Q = 5 * 10**4


def generate(rng):
    ends = pick_shape(rng) != 2
    colors = [rng.randint(1, 2) for _ in range(N)]
    if ends:
        colors[0] = colors[-1] = 3
    queries = [
        [rng.randrange(N), 3 if rng.random() < 0.95 else rng.randint(1, 2)] for _ in range(Q)
    ]
    return {"colors": colors, "queries": queries}
