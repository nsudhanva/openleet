"""Maximum Number of K-Divisible Components on a 2 * 10^4-node tree: a path of 1.8 * 10^4 nodes
with the rest hung off it, so summing each node's subtree separately is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    k = rng.randint(2, 1000)
    spine = N * 9 // 10
    parent = [-1] + [i - 1 if i < spine else rng.randrange(i) for i in range(1, N)]
    label = list(range(N))
    rng.shuffle(label)
    edges = [[label[i], label[parent[i]]] for i in range(1, N)]
    for e in edges:
        if rng.random() < 0.5:
            e.reverse()
    rng.shuffle(edges)
    values = [
        rng.randrange(10**9 // k) * k if rng.random() < 0.5 else rng.randint(0, 10**9)
        for _ in range(N)
    ]
    # Make the total divisible by k by lowering one node that has room.
    r = sum(values) % k
    i = next(i for i in range(N) if values[i] >= r)
    values[i] -= r
    return {"n": N, "edges": edges, "values": values, "k": k}
