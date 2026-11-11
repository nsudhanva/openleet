"""All Paths From Source Lead to Destination at 10^4 edges: a chain of 2500 diamonds (2^2500
source-destination paths, every one ending at the destination), node labels shuffled, so a
search that does not remember finished nodes walks paths without end."""

SEEDS = 2
N = 10**4
DIAMONDS = 2500


def generate(rng):
    label = list(range(N))
    rng.shuffle(label)
    edges = []
    for d in range(DIAMONDS):
        a, b, c, e = 3 * d, 3 * d + 1, 3 * d + 2, 3 * d + 3
        edges += [[a, b], [a, c], [b, e], [c, e]]
    edges = [[label[u], label[v]] for u, v in edges]
    rng.shuffle(edges)
    return {"n": N, "edges": edges, "source": label[0], "destination": label[3 * DIAMONDS]}
