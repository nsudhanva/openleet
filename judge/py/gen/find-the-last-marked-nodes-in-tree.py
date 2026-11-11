"""Find the Last Marked Nodes in Tree at n = 5000: an even-length spine with shorter random
branches, so every node's farthest node is unique, and a BFS from every node is
~2.5 * 10^7 steps."""

SEEDS = 2
N = 5000


def generate(rng):
    spine = rng.randrange(N // 4, N // 2) * 2
    # Node i < spine sits on the path 0 - 1 - ... - spine - 1. A branch node hangs off spine
    # node p at depth d < min(p, spine - 1 - p), so the two path ends stay the only farthest
    # nodes and, the path having an odd number of edges, never tie.
    where = [(i, 0) for i in range(spine)]
    edges = [[i - 1, i] for i in range(1, spine)]
    for v in range(spine, N):
        while True:
            u = rng.randrange(v)
            p, depth = where[u]
            if depth + 1 < min(p, spine - 1 - p):
                break
        where.append((p, depth + 1))
        edges.append([u, v])
    labels = list(range(N))
    rng.shuffle(labels)
    edges = [
        [labels[a], labels[b]] if rng.random() < 0.5 else [labels[b], labels[a]] for a, b in edges
    ]
    rng.shuffle(edges)
    return {"edges": edges}
