"""Paths in Maze That Lead to Same Room at the maximum 1000 rooms with 5000 corridors, a few
hundred triangles planted, so checking every triple of rooms does ~1.7 * 10^8 steps where
pairing neighbors does ~10^5."""

SEEDS = 2
N = 1000
M = 5000


def generate(rng):
    edges = set()

    def add(a, b):
        edges.add((min(a, b), max(a, b)))

    while len(edges) < M // 2:
        a, b, c = rng.sample(range(1, N + 1), 3)
        add(a, b), add(b, c), add(a, c)
    while len(edges) < M:
        a, b = rng.sample(range(1, N + 1), 2)
        add(a, b)
    corridors = [list(e) if rng.random() < 0.5 else [e[1], e[0]] for e in sorted(edges)]
    rng.shuffle(corridors)
    return {"n": N, "corridors": corridors[:M]}
