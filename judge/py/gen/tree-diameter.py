"""Tree Diameter at the full 10^4 nodes: a long path with short branches, so a BFS from every node
is ~10^8 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    label = rng.sample(range(N), N)
    edges = []
    for i in range(1, N):
        p = i - 1 if rng.random() < 0.7 else rng.randrange(max(0, i - 20), i)
        e = [label[p], label[i]]
        rng.shuffle(e)
        edges.append(e)
    rng.shuffle(edges)
    return {"edges": edges}
