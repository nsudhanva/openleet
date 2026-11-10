"""Possible Bipartition at n = 2000 with 10^4 unique dislikes: a hidden bipartite split
(true), or the same plus one odd cycle buried deep in a component (false)."""

SEEDS = 2
N = 2000
M = 10**4


def generate(rng):
    side = [rng.randint(0, 1) for _ in range(N + 1)]
    pairs = set()
    while len(pairs) < M - 1:
        a, b = rng.randint(1, N), rng.randint(1, N)
        if a != b and side[a] != side[b]:
            pairs.add((min(a, b), max(a, b)))
    if rng.random() < 0.5:
        while True:
            a, b = rng.randint(1, N), rng.randint(1, N)
            if a != b and side[a] == side[b]:
                pairs.add((min(a, b), max(a, b)))
                break
    else:
        while len(pairs) < M:
            a, b = rng.randint(1, N), rng.randint(1, N)
            if a != b and side[a] != side[b]:
                pairs.add((min(a, b), max(a, b)))
    dislikes = [list(p) for p in sorted(pairs)]
    rng.shuffle(dislikes)
    return {"n": N, "dislikes": dislikes}
