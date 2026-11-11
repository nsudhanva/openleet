"""Distance to a Cycle in Undirected Graph at n = 2 * 10^4: a short cycle with a few long
chains hanging off it, so a search from every node to the cycle is 5 * 10^7 to 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    cycle = rng.randint(3, 10)
    label = list(range(N))
    rng.shuffle(label)
    edges = [[label[i], label[(i + 1) % cycle]] for i in range(cycle)]
    chains = rng.randint(1, 4)
    node = cycle
    for c in range(chains):
        length = (N - cycle) // chains if c < chains - 1 else N - node
        prev = rng.randrange(cycle)
        for _ in range(length):
            edges.append([label[prev], label[node]])
            prev = node
            node += 1
    for e in edges:
        if rng.random() < 0.5:
            e.reverse()
    rng.shuffle(edges)
    return {"n": N, "edges": edges}
