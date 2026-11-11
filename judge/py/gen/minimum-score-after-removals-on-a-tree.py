"""Minimum Score After Removals on a Tree with 500 nodes in a random tree, so removing each of the
~1.2 * 10^5 edge pairs and recomputing the three component XORs by a traversal is cubic against
the quadratic subtree-XOR pass."""

SEEDS = 2
N = 500
LIMIT = 10**8


def generate(rng):
    order = list(range(N))
    rng.shuffle(order)
    edges = [[order[rng.randrange(i)], order[i]] for i in range(1, N)]
    for e in edges:
        if rng.random() < 0.5:
            e.reverse()
    rng.shuffle(edges)
    return {"nums": [rng.randint(1, LIMIT) for _ in range(N)], "edges": edges}
