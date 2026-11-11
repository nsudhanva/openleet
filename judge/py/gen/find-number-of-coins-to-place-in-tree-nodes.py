"""Find Number of Coins to Place in Tree Nodes at n = 2 * 10^4 on a long path with short
side branches, so collecting and sorting every subtree's costs is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    edges = []
    for v in range(1, N):
        u = v - 1 if rng.random() < 0.9 else rng.randrange(max(0, v - 5), v)
        edges.append([u, v] if rng.random() < 0.5 else [v, u])
    rng.shuffle(edges)
    cost = [rng.randint(1, 10**4) * rng.choice((1, -1)) for _ in range(N)]
    return {"edges": edges, "cost": cost}
