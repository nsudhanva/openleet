"""Maximum Score After Applying Operations on a Tree with 2 * 10^4 nodes: a path of 1.8 * 10^4
nodes with the rest hung off it, so summing each subtree separately is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    spine = N * 9 // 10
    parent = [-1] + [i - 1 if i < spine else rng.randrange(i) for i in range(1, N)]
    label = list(range(1, N))
    rng.shuffle(label)
    label = [0, *label]  # node 0 stays the root
    edges = [[label[i], label[parent[i]]] for i in range(1, N)]
    for e in edges:
        if rng.random() < 0.5:
            e.reverse()
    rng.shuffle(edges)
    return {"edges": edges, "values": [rng.randint(1, 10**9) for _ in range(N)]}
