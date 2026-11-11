"""Number of Nodes in the Sub-Tree With the Same Label at 2 * 10^4 nodes, each hanging off the
previous node or one a few back, so the tree is ~1.4 * 10^4 deep and walking every node's subtree
to count its label costs ~10^8 visits."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    ids = [0, *rng.sample(range(1, N), N - 1)]
    edges = []
    for v in range(1, N):
        parent = max(0, v - 1 - (rng.randrange(5) if rng.random() < 0.2 else 0))
        a, b = ids[parent], ids[v]
        edges.append([a, b] if rng.random() < 0.5 else [b, a])
    rng.shuffle(edges)
    alphabet = "abcdefghijklmnopqrstuvwxyz"[: rng.randint(2, 6)]
    labels = "".join(rng.choice(alphabet) for _ in range(N))
    return {"n": N, "edges": edges, "labels": labels}
