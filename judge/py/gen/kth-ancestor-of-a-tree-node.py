"""Kth Ancestor at n = 5 * 10^4 with 5 * 10^4 queries: a single long chain (walking up k
steps per query is quadratic) or a random tree with mostly-deep queries."""

SEEDS = 2
N = 5 * 10**4
QUERIES = 5 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        parent = [-1, *list(range(N - 1))]
    else:
        parent = [-1] + [rng.randrange(max(0, i - 50), i) for i in range(1, N)]
    ops, args = ["TreeAncestor"], [[N, parent]]
    for _ in range(QUERIES):
        node = rng.randrange(N)
        k = rng.randint(1, N) if rng.random() < 0.2 else rng.randint(1, max(1, node))
        ops.append("getKthAncestor")
        args.append([node, k])
    return {"ops": ops, "args": args}
