"""Equal Tree Partition with 10^4 nodes in a chain (each child on a random side), with an even
total that no subtree halves, so recomputing a subtree sum below every node is ~5 * 10^7
steps."""

from _shapes import level_order, shaped_tree

SEEDS = 2
N = 10**4
LIMIT = 10**5


def generate(rng):
    left, right = shaped_tree(rng, N, "chain")
    vals = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    # Subtree sums, children before parents (node ids grow away from the root).
    sums = list(vals)
    parent = [0] * N
    for v in range(N):
        for child in (left[v], right[v]):
            if child is not None:
                parent[child] = v
    for v in range(N - 1, 0, -1):
        sums[parent[v]] += sums[v]
    below = set(sums[1:])
    root = vals[0]
    while True:
        total = sums[0] - vals[0] + root
        if total % 2 == 0 and total // 2 not in below and -LIMIT <= root <= LIMIT:
            break
        root = rng.randint(-LIMIT, LIMIT)
    vals[0] = root
    return {"root": level_order(vals, left, right)}
