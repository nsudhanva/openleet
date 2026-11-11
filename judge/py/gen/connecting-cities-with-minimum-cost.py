"""Connecting Cities With Minimum Cost with 10^4 connections: a spanning tree of 10^4 cities
(path-like or random) plus one extra edge, or a star on 6667 cities whose edges, cheapest first,
grow a union-find chain when roots are never balanced, plus extra edges between the first leaves
just before the last star edge; Prim's O(n) minimum scan per step costs ~10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
E = 10**4
STAR = 6667


def tree(rng):
    chain = 0.9 if rng.random() < 0.5 else 0.1
    labels = list(range(1, N + 1))
    rng.shuffle(labels)
    pairs = []
    for v in range(1, N):
        u = v - 1 if rng.random() < chain else rng.randrange(v)
        pairs.append((labels[u], labels[v]))
    while len(pairs) < E:
        a, b = rng.sample(labels, 2)
        pairs.append((a, b))
    rng.shuffle(pairs)
    return {"n": N, "connections": [[a, b, rng.randint(0, 10**5)] for a, b in pairs]}


def star(rng, center_first):
    labels = list(range(1, STAR + 1))
    rng.shuffle(labels)
    center, leaves = labels[0], labels[1:]
    top = 10**5
    costs = [*sorted(rng.sample(range(top - 1), len(leaves) - 1)), top]
    pairs = zip(leaves, costs, strict=True)
    edges = [[center, k, c] if center_first else [k, center, c] for k, c in pairs]
    early, extra = 1, E - len(edges)
    while early * (early - 1) // 2 < extra:
        early += 1
    extras = [(a, b) for b in range(early) for a in range(b)][:extra]
    edges += [[leaves[a], leaves[b], top - 1] for a, b in extras]
    rng.shuffle(edges)
    return {"n": STAR, "connections": edges}


def generate(rng):
    shape = pick_shape(rng)
    return tree(rng) if shape == 0 else star(rng, shape == 1)
