"""Maximum Star Sum of a Graph at n = 3 * 10^4 nodes and 3 * 10^4 random edges, so gathering each
centre's neighbours by scanning the edge list costs ~10^9 steps."""

SEEDS = 2
N = 3 * 10**4
E = 3 * 10**4


def generate(rng):
    edges, seen = [], set()
    while len(edges) < E:
        a, b = rng.randrange(N), rng.randrange(N)
        if a != b and (min(a, b), max(a, b)) not in seen:
            seen.add((min(a, b), max(a, b)))
            edges.append([a, b])
    vals = [rng.randint(-(10**4), 10**4) for _ in range(N)]
    return {"vals": vals, "edges": edges, "k": rng.randint(1, 5)}
