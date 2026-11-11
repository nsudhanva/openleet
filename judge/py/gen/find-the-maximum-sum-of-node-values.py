"""Find the Maximum Sum of Node Values on a 1000-node random tree, so trying every set of
edges to operate on is 2^999 while the parity DP is linear."""

SEEDS = 2
N = 1000


def generate(rng):
    nums = [rng.randint(0, 10**9) for _ in range(N)]
    edges = []
    for v in range(1, N):
        u = rng.randrange(v)
        edges.append([u, v] if rng.random() < 0.5 else [v, u])
    rng.shuffle(edges)
    return {"nums": nums, "k": rng.randint(1, 10**9), "edges": edges}
