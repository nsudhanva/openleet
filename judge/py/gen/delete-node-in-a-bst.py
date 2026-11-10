"""Delete Node in a BST with 10^4 unique values: a degenerate chain with the key at the deep
end, or a random BST whose key
(a node with at most one child, so the result is unique) is present or absent."""

from _shapes import level_order

SEEDS = 3
N = 10**4


def generate(rng):
    vals = rng.sample(range(-(10**5), 10**5 + 1), N)
    left, right = [-1] * N, [-1] * N
    if rng.random() < 0.4:
        vals.sort(reverse=rng.random() < 0.5)
        child = left if vals[0] > vals[1] else right
        for i in range(N - 1):
            child[i] = i + 1
        key = vals[rng.randrange(N - 10, N)]
    else:
        for i in range(1, N):
            u = 0
            while True:
                side = left if vals[i] < vals[u] else right
                if side[u] < 0:
                    side[u] = i
                    break
                u = side[u]
        if rng.random() < 0.7:
            # A node with at most one child: every correct deletion gives the same tree.
            key = vals[rng.choice([i for i in range(N) if left[i] < 0 or right[i] < 0])]
        else:
            present = set(vals)
            key = rng.randint(-(10**5), 10**5)
            while key in present:
                key = rng.randint(-(10**5), 10**5)
    return {"root": level_order(vals, left, right, empty=-1), "key": key}
