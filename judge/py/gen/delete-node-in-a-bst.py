"""Delete Node in a BST with 10^4 unique values: a degenerate chain with the key at the deep
end, or a random BST whose key
(a node with at most one child, so the result is unique) is present or absent."""

from _shapes import insert_bst, level_order

SEEDS = 3
N = 10**4


def generate(rng):
    vals = rng.sample(range(-(10**5), 10**5 + 1), N)
    chain = rng.random() < 0.4
    if chain:
        vals.sort(reverse=rng.random() < 0.5)
    left, right = insert_bst(vals, range(N))
    if chain:
        key = vals[rng.randrange(N - 10, N)]
    elif rng.random() < 0.7:
        # A node with at most one child: every correct deletion gives the same tree.
        key = vals[rng.choice([i for i in range(N) if left[i] is None or right[i] is None])]
    else:
        present = set(vals)
        key = rng.randint(-(10**5), 10**5)
        while key in present:
            key = rng.randint(-(10**5), 10**5)
    return {"root": level_order(vals, left, right), "key": key}
