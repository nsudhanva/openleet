"""Maximum Score of a Node Sequence with two adjacent hubs of 1.2 * 10^4 leaves each (shuffled
labels), so pairing every neighbour of both ends of the hub edge costs ~1.4 * 10^8 steps."""

SEEDS = 2
LEAVES = 12000


def generate(rng):
    n = 2 * LEAVES + 2
    label = rng.sample(range(n), n)
    edges = [[label[0], label[1]]]
    for v in range(2, n):
        edges.append([label[v % 2], label[v]])
    rng.shuffle(edges)
    for e in edges:
        if rng.random() < 0.5:
            e.reverse()
    return {"scores": [rng.randint(1, 10**8) for _ in range(n)], "edges": edges}
