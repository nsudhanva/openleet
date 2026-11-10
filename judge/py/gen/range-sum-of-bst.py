"""Range Sum of BST with 2 * 10^4 unique values: a random BST, or a nearly linear one 20,000
levels deep; the range covers a middle slice."""

from _shapes import insert_bst, level_order

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    vals = rng.sample(range(1, 10**5 + 1), N)
    if rng.random() < 0.5:
        order = range(N)
    else:
        # A zigzag chain: alternate taking the smallest and largest remaining value.
        by_val = sorted(range(N), key=lambda i: vals[i])
        lo, hi, order = 0, N - 1, []
        while lo <= hi:
            order.append(by_val[lo])
            lo += 1
            if lo <= hi:
                order.append(by_val[hi])
                hi -= 1
    left, right = insert_bst(vals, order)
    low = rng.randint(1, 4 * 10**4)
    root = level_order(vals, left, right, order[0])
    return {"root": root, "low": low, "high": rng.randint(low, 10**5)}
