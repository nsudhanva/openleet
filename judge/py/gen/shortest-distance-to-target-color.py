"""Shortest Distance to Target Color with 2 * 10^4 colors and queries: color 3 sits only at the
two ends (or nowhere) and almost every query asks for it, so scanning outward per query is ~n
steps each."""

SEEDS = 2
N = 2 * 10**4
Q = 2 * 10**4


def generate(rng):
    colors = [rng.randint(1, 2) for _ in range(N)]
    if rng.random() < 0.5:
        colors[0] = colors[-1] = 3
    queries = [
        [rng.randrange(N), 3 if rng.random() < 0.95 else rng.randint(1, 2)] for _ in range(Q)
    ]
    return {"colors": colors, "queries": queries}
